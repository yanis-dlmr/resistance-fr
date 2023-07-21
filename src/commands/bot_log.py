import os
import re

from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

from ..helper import *
from ..helper.logger import logger as log
from ..messages import *

__all__ = ['BotLog']


@app_commands.default_permissions(administrator=True)
class BotLog(commands.GroupCog):

  def __init__(self, client: commands.AutoShardedBot):
    self.__client = client # pylint: disable=unused-private-member
    log.info('BotLog cog loaded !')

  @app_commands.command(name='help', description='Get help about a command')
  async def help(self, interaction: discord.Interaction):
    embed = build_help_embed(
      title='Help for `BotLog` group',
      description='`BotLog` group contains commands that are useful for the bot owner.',
    ).add_field(
      name='📝 `dump`',
      value='Dump the bot log in the current channel.',
      inline=False,
    ).add_field(
      name='🔎 `filter`',
      value='Filter the bot log based on some expressions and a mode.'
      '"all" mode means that all expressions must be found in a chunk, "any" mode means that at least one expression must be found in a chunk.'
      'A chunk is a log between two timestamps, so that full error messages are preserved.',
      inline=False,
    ).add_field(
      name='♻️ `last`',
      value='Get the last few lines of the bot logs (defaults to 10).',
      inline=False,
    )

    await reply_with_embed(interaction, embed)

  @app_commands.command(name='dump', description='Dump the bot log 📝')
  async def dump(self, interaction: discord.Interaction):
    file = discord.File('bot.log')
    embed = build_success_embed(title=f'{SUCCESS_EMOJI} bot log dumped !',)
    try:
      await send_channel_file(interaction.channel, file)
    except Exception as e:                           # pylint: disable=broad-except
      embed = build_error_embed(
        title=f'{FAIL_EMOJI} bot log dump failed !',
        description=f'```{e}```',
      )
    await reply_with_embed(interaction, embed)

  @app_commands.command(name='filter', description='Filter the bot log based on some expressions 🔎')
  @app_commands.describe(
    expressions='Words or regex expressions (csv) to filter the bot log with',
    mode='Mode of the filter (all or any, defaults to any)',
  )
  @app_commands.choices(
    mode=[app_commands.Choice(name='all', value=0),
          app_commands.Choice(name='any', value=1)])
  async def filter(
    self,
    interaction: discord.Interaction,
    expressions: str,
    mode: Optional[app_commands.Choice[int]] = None,
  ):
    expressions: list[str] = expressions.split(',')
    expressions = [expression.strip().lower() for expression in expressions]
    if mode is None:
      mode = app_commands.Choice(name='any', value=1)

    embed = build_success_embed(
      title=f'{SUCCESS_EMOJI} bot log filtered !',
      description=f'```{mode.name} {expressions}```',
    )

    try:
      # there are so many things that can go wrong here...

      # read the file chunk by chunk
      # each chunk is all the lines that are between two timestamps

      with open('bot.log', 'r', encoding='utf-8') as f:
        lines = f.readlines()

      chunks: list[str] = []
      for line in lines:
        # timestamp is : '%Y-%m-%d %H:%M:%S' and is located anywhere in the line
        if re.match('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line):
          chunks.append(line)
        elif len(chunks) == 0:
          chunks.append(line)
        else:
          chunks[-1] += line
      fmode = all if mode.value == 0 else any

      new_file: list[str] = [c for c in chunks if fmode([e in c.lower() for e in expressions])]

      with open('tmp.bot.log', 'w', encoding='utf-8') as f:
        f.writelines(new_file)
      file = discord.File('tmp.bot.log')
      await send_channel_file(interaction.channel, file)
      os.remove('tmp.bot.log')

    except Exception as e: # pylint: disable=broad-except

      embed = build_error_embed(
        title=f'{FAIL_EMOJI} bot log filter failed !',
        description=f'```{e}```',
      )
    await reply_with_embed(interaction, embed)

  @app_commands.command(name='last', description='Get the last lines of the bot log ♻️')
  @app_commands.describe(
    lines='Number of lines to get (defaults to 10)',)
  @app_commands.choices(
    lines=[app_commands.Choice(name=str(i), value=i) for i in (1, 10, 20, 50, 100)],)
  async def last(self, interaction: discord.Integration, lines: Optional[app_commands.Choice[int]] = None):
    if lines is None:
      lines = app_commands.Choice(name='10', value=10)

    # for this request we will build the success embed after the request

    try:
      # there are so many things that can go wrong here...
      with open('bot.log', 'r', encoding='utf-8') as f:
        file_lines = f.readlines()

      new_file: list[str] = file_lines[-lines.value:]

      with open('tmp.bot.log', 'w', encoding='utf-8') as f:
        f.writelines(new_file)
      file = discord.File('tmp.bot.log')
      await send_channel_file(interaction.channel, file)
      os.remove('tmp.bot.log')

    except Exception as e: # pylint: disable=broad-except

      embed = build_error_embed(
        title=f'{FAIL_EMOJI} bot log filter failed !',
        description=f'```{e}```',
      )
    else:
      embed = build_success_embed(
        title=f'{SUCCESS_EMOJI} bot log filtered !',
        description=f'```got {(n:=len(new_file))}/{lines.value} line{"s" if n > 1 else ""}```',
      )
    await reply_with_embed(interaction, embed)
