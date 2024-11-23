from typing import Any

from discord import app_commands
from discord.ext import commands

from ..db import *
from ..helper import *


@app_commands.default_permissions(manage_guild=True)
class Config(UsefullCog):
  
  def __init__(self, client: commands.AutoShardedBot, db: UsefulDatabase):
    self.__db = db
    super().__init__(client)
  
  @app_commands.command(name='help', description='Get or set a configuration value')
  async def help(self, interaction: discord.Interaction):
    embed = self.embed_builder.build_help_embed(
      title='Help for `Config` group',
      description='`Config` group contains commands that are useful for configuring the bot.',
    ).add_field(
      name='🔧 `get`',
      value='Get a configuration value.',
      inline=False,
    ).add_field(
      name='🔧 `set`',
      value='Set a configuration value.',
      inline=False,
    )
    await self.dispatcher.reply_with_embed(interaction, embed)
    self.log_interaction(interaction)
  
  @app_commands.command(name='get', description='Get a configuration value 🔧')
  async def get(self, interaction: discord.Interaction, key: str = None):
    config = list(self.__db.get_config())[0]
    if key is None: # Display the entire configuration
      embed = self.embed_builder.build_info_embed(
        title='Configuration values',
        description='\n'.join([f'{k} : {v}' for k, v in config.items()]),
      )
      await self.dispatcher.reply_with_embed(interaction, embed)
      self.log_interaction(interaction)
      return
    else:
      value = config[key]
      if value is None:
        embed = self.embed_builder.build_error_embed(
          title='Configuration value not found',
          description=f'Configuration value `{key}` not found.',
        )
      else:
        embed = self.embed_builder.build_info_embed(
          title=f'Configuration value `{key}`',
          description=value,
        )
      await self.dispatcher.reply_with_embed(interaction, embed)
      self.log_interaction(interaction)