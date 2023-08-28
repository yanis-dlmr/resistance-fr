import logging

import discord
from discord.ext import commands

from ..messages import MessageSender, Embedder

__all__ = ['UsefullCog']


class UsefullCog(commands.GroupCog):

  def __init__(self, client: commands.AutoShardedBot) -> None:
    self.client = client
    self.dispatcher: MessageSender = client.dispatcher
    self.embed_builder: Embedder = client.embed_builder

    self.log = logging.getLogger(f'cogs.{self.__class__.__name__.lower()}')

  @commands.Cog.listener()
  async def on_ready(self):
    self.log.info('%s cog loaded !', self.__class__.__name__)

  def log_interaction(self, interaction: discord.Interaction):
    self.log.debug('[%s] %s#%s - %s(%s)', interaction.guild.name, interaction.user.name,
                   interaction.user.discriminator, interaction.command.name, self.__class__.__name__.lower())
