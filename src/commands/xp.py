from typing import Callable

import discord
from discord import app_commands
from discord.ext import commands

from ..db import *
from ..helper import *
from ..helper.logger import logger as log
from ..messages import *

__all__ = ['Xp']


class LeaderBoardView(CustomView):

  items_per_page = 10

  def __init__(
    self,
    orig_inter: discord.Integration,
    embed: discord.Embed,
    client: commands.AutoShardedBot,
    db: UsefulDatabase,
    timeout: int | None = 180,
  ):
    super().__init__(orig_inter, timeout)

    self.with_button_callback("⬅️", callback=self.__on_page_change(-1))
    self.with_button_callback("➡️", callback=self.__on_page_change(1))

    self.embed = embed
    self.items: dict[int, str] = {}

    self.__tmp_records: list[ExportUserEntry] = None
    self.__client = client
    self.__db = db
    self.__page = 0

    self.__setup()

  @property
  def first_page(self) -> str:
    return self.items[0]

  @property
  def n_pages(self) -> int:
    return len(self.items)

  def wrap_page_no(self, page: int) -> int:
    return page % self.n_pages

  def __setup(self) -> None:
    self.__tmp_records = list(self.__db.users())
    self.__tmp_records.sort(key=lambda e: e.xp, reverse=True)

    building_page = 0
    current_page = ''
    i = 0
    for entry in self.__tmp_records:
      user = self.interaction.guild.get_member(entry.id)
      xp = entry.xp
      if user is None or xp < 0:
        continue
      i += 1
      line = f'{i}. `{user.display_name}` ({user.mention}) {xp} XP ({self.__client.xp_to_lvl(xp)})\n'
      current_page += line

      if i % self.items_per_page == 0:
        self.items.update({building_page: current_page})
        current_page = ''
        building_page += 1

    if current_page != '':
      self.items.update({building_page: current_page})

  def __on_page_change(self, page: int) -> Callable[[discord.Interaction], None]:

    async def callback(interaction: discord.Interaction) -> None:
      await interaction.response.defer()
      self.__page = self.wrap_page_no(self.__page + page)

      self.embed.description = self.items[self.__page]
      self.embed.set_footer(text=f'Page {self.__page + 1}/{self.n_pages}')
      await self.interaction.edit_original_response(embed=self.embed, view=self)

    return callback


class Xp(commands.GroupCog):

  def __init__(self, client: commands.AutoShardedBot, db: UsefulDatabase):
    self.__client = client
    self.__db = db
    log.info('Xp cog loaded !')

  @app_commands.command(name='help', description='Get help about a command')
  async def help(self, interaction: discord.Interaction):
    embed = build_help_embed(
      title='Help for `Xp` group',
      description='`Xp` group contains commands that allow you to get insight about your XP in the server.',
    ).add_field(
      name='🕵️ `me`',
      value='Get your XP in the server (private mode).',
      inline=False,
    ).add_field(
      name='👤 `user`',
      value='Get the XP of a user in the server (public mode).',
      inline=False,
    ).add_field(
      name='📊 `leaderboard`',
      value='Get the XP leaderboard of the server.',
      inline=False,
    ).add_field(
      name='📊 `no_life`',
      value='Alias to top 3 of `leaderboard`.',
      inline=False,
    )
    await reply_with_embed(interaction, embed)

  @app_commands.command(name='me', description='Get your XP in the server 🕵️')
  async def me(self, interaction: discord.Interaction):
    user = interaction.user
    xp = self.__db.get_user_xp(user.id)
    failed = False
    embed = build_info_embed(
      title=f'Your XP in {interaction.guild.name}',
      description=f'{interaction.user.display_name} ({user.mention}) : {xp} XP ({self.__client.xp_to_lvl(xp)})'
    )
    if xp < 0:
      failed = True
      embed = build_error_embed(
        title=f'You do not have any XP in {interaction.guild.name}',
        description='Please let an admin know about this issue.',
      )
    await reply_with_status_embed(interaction, embed, failed=failed)

  @app_commands.command(name='user', description='Get the XP of a user in the server 👤')
  async def user(self, interaction: discord.Interaction, user: discord.Member):
    xp = self.__db.get_user_xp(user.id)
    embed = build_info_embed(
      title=f'XP of {user.display_name} in {interaction.guild.name}',
      description=
      f'{interaction.user.display_name} ({user.mention}) : {xp} XP ({self.__client.xp_to_lvl(xp)})',
    )
    if xp < 0:
      embed = build_error_embed(
        title=f'{user.display_name} does not have any XP in {interaction.guild.name}',
        description='Please let an admin know about this issue.',
      )
    await reply_with_embed(interaction, embed)

  @app_commands.command(name='leaderboard', description='Get the XP leaderboard of the server 📊')
  async def leaderboard(self, interaction: discord.Interaction):
    embed: discord.Embed = None
    view: LeaderBoardView = None
    followup = True
    try:
      embed = build_info_embed(
        title=f'📊 Leaderboard of {interaction.guild.name}',
        description='...loading...',
      )
      view = LeaderBoardView(interaction, embed, self.__client, self.__db)
      await send_xp_embed(interaction, embed, view)

    except Exception as e: # pylint: disable=broad-except

      followup = False
      embed = build_error_embed(
        title='Oopsie, something went wrong !',
        description=f'Please let an admin know about this issue : \n```py\n{e.with_traceback(None)}\n```',
      )
      await reply_with_embed(interaction, embed)

    if followup:
      first_page = view.first_page
      embed.description = first_page
      embed.set_footer(text=f'Page 1/{view.n_pages}')
      await interaction.edit_original_response(embed=embed, view=view)

  @app_commands.command(name='no_life', description='Alias to top 3 of `leaderboard` 📊')
  async def no_life(self, interaction: discord.Interaction):
    embed: discord.Embed = None
    try:
      embed = build_info_embed(
        title=f'Top 3 of {interaction.guild.name}',
        description=':flag_fr: les pires no-lifes du serveur :flag_fr:',
      )
      # do not change the "3" 🥲
      for i, user_entry in enumerate(self.__db.top_users(3)):
        user = interaction.guild.get_member(user_entry.id)
        xp = user_entry.xp
        embed.add_field(
          name='',
          value=
          f'{TROPHY_EMOJIS[i]} `{user.display_name}` ({user.mention}) {xp} XP ({self.__client.xp_to_lvl(xp)})',
          inline=False,
        )

    except Exception as e: # pylint: disable=broad-except

      embed = build_error_embed(
        title='Oopsie, something went wrong !',
        description='Please let an admin know about this issue : \n```py\n' + str(e) + '\n```',
      )
    await reply_with_embed(interaction, embed)
