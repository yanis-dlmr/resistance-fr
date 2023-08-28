import datetime

import discord
from discord import app_commands

from ..helper import *

__all__ = ['Sudo']


@app_commands.default_permissions(manage_guild=True, moderate_members=True, ban_members=True)
class Sudo(UsefullCog):

  @app_commands.command(name='help', description='Get help about a command')
  async def help(self, interaction: discord.Interaction):
    embed = self.embed_builder.build_help_embed(
      title='Help for `Sudo` group',
      description='`Sudo` group contains commands that are useful for guild administrators.',
    ).add_field(
      name='🤫 `echo`',
      value='Echo a message as the bot.',
      inline=False,
    ).add_field(
      name='📝 `edit`',
      value='Edit the last text message the bot sent in the channel (fetches the last 100 messages).',
      inline=False,
    ).add_field(
      name='🔨 `timeout`',
      value='Timeout a specific user for a given duration (reason is optional).',
      inline=False,
    ).add_field(
      name='🔨 `untimeout`',
      value='Remove a timeout completely from a specific user.',
      inline=False,
    ).add_field(
      name='🦶 `kick`',
      value='Kick a specific user from the guild (reason is optional).',
      inline=False,
    ).add_field(
      name='🚫 `ban`',
      value='Ban a specific user from the guild (reason is optional).',
      inline=False,
    ).add_field(
      name='🚫 `unban`',
      value=
      'Unban a specific user from the guild (**caution**: be sure that you want to unban this user, as the user will be able to join the guild again and could even use old links).',
      inline=False,
    )
    await self.dispatcher.reply_with_embed(interaction, embed)
    self.log_interaction(interaction)

  @app_commands.command(name='echo', description='Echo a message 🤫')
  async def echo(self, interaction: discord.Interaction, message: str):
    embed = self.embed_builder.build_success_embed(title=f'{SUCCESS_EMOJI} message sent !',)
    await self.dispatcher.send_channel_message(interaction.channel, message)
    await self.dispatcher.reply_with_status_embed(interaction, embed)
    self.log_interaction(interaction)

  @app_commands.command(name='edit', description='Edit the last message the bot sent in the channel 📝')
  async def edit(self, interaction: discord.Interaction, message: str):
    embed = self.embed_builder.build_success_embed(title=f'{SUCCESS_EMOJI} message edited !',)
    failed, found = False, False

    async for msg in interaction.channel.history(limit=100):
      if msg.author == self.client.user and len(msg.embeds) == 0:
        found = True                    # found a message to edit
        await msg.edit(content=message) # if this fails, the exception will be caught
        break

    if not found:
      # won't be executed if an exception was raised
      failed = True
      embed = self.embed_builder.build_error_embed(
        title=f'{FAIL_EMOJI} error while editing message !',
        description='```No editable text message found.```',
      )
    await self.dispatcher.reply_with_status_embed(interaction, embed, failed)
    self.log_interaction(interaction)

  @app_commands.command(name='timeout', description='Timeout a user 🔨')
  @app_commands.describe(
    user='User to timeout',
    duration='Duration of the timeout',
    reason='Reason for the timeout (optional)',
  )
  @app_commands.choices(duration=[
    app_commands.Choice(name='1 minute', value=60),
    app_commands.Choice(name='30 minutes', value=1800),
    app_commands.Choice(name='1 hour', value=3600),
    app_commands.Choice(name='3 hours', value=10800),
    app_commands.Choice(name='12 hours', value=43200),
    app_commands.Choice(name='1 day', value=86400),
    app_commands.Choice(name='3 days', value=259200),
    app_commands.Choice(name='1 week', value=604800),
    app_commands.Choice(name='3 weeks', value=1814400),
  ])
  async def timeout(
    self,
    interaction: discord.Interaction,
    user: discord.Member,
    duration: app_commands.Choice[int],
    reason: str | None = None,
  ):
    embed = self.embed_builder.build_success_embed(
      title=f'{SUCCESS_EMOJI} user `{user}` has been timed out for `{duration.name}` !',)
    failed = False
    delta = datetime.timedelta(seconds=duration.value)
    await user.timeout(delta, reason=reason)

    await self.dispatcher.reply_with_status_embed(interaction, embed, failed)
    self.log_interaction(interaction)

  @app_commands.command(name='untimeout', description='Untimeout a user 🔨')
  @app_commands.describe(user='User to untimeout',)
  async def untimeout(self, interaction: discord.Interaction, user: discord.Member):
    embed = self.embed_builder.build_success_embed(
      title=f'{SUCCESS_EMOJI} user `{user}` has been untimed out !',)
    await user.timeout(None)
    await self.dispatcher.reply_with_status_embed(interaction, embed)
    self.log_interaction(interaction)

  @app_commands.command(name='kick', description='Kick a user 🦶')
  @app_commands.describe(
    user='User to kick',
    reason='Reason for the kick (optional)',
  )
  async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str | None = None):
    embed = self.embed_builder.build_success_embed(title=f'{SUCCESS_EMOJI} user `{user}` has been kicked !',)
    await user.kick(reason=reason)
    await self.dispatcher.reply_with_status_embed(interaction, embed)
    self.log_interaction(interaction)

  @app_commands.command(name='ban', description='Ban a user 🚫')
  @app_commands.describe(
    user='User to ban',
    reason='Reason for the ban (optional)',
    del_msgs='Should the messages of the user be deleted ? (default: False)',
  )
  async def ban(self,
                interaction: discord.Interaction,
                user: discord.Member,
                reason: str | None = None,
                del_msgs: bool = False):
    embed = self.embed_builder.build_success_embed(title=f'{SUCCESS_EMOJI} user `{user}` has been banned !',)
    await user.ban(reason=reason, delete_message_days=7 if del_msgs else 0)
    await self.dispatcher.reply_with_status_embed(interaction, embed)
    self.log_interaction(interaction)

  @app_commands.command(name='unban', description='Unban a user 🚫')
  @app_commands.describe(
    user='User to unban',
    reason='Reason for the unban (optional)',
  )
  async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str | None = None):
    embed = self.embed_builder.build_success_embed(
      title=f'{SUCCESS_EMOJI} user `{user}` has been unbanned !',)
    await interaction.guild.unban(user, reason=reason)
    await self.dispatcher.reply_with_status_embed(interaction, embed)
    self.log_interaction(interaction)
