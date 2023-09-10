import signal
import sys
import os

import logging
import datetime
import math
from functools import lru_cache

from typing import Any
from typing_extensions import override

from pyjson5 import decode_io, encode_io # pylint: disable=no-name-in-module
import discord
from discord.ext import commands
from discord.message import Message

from ..helper import *
from ..helper.logger import init_logger
from ..messages import MessageSender, Embedder
from ..commands import *
from ..db import *
from ..events import TaskManager

from ..version import __version__

__all__ = ['UsefulClient']


class ChannelToLastMessageInfo:
  file_path = 'data/last_message.json5'
  lmi = dict[str, int | float]

  def __init__(self) -> None:
    os.makedirs('data', exist_ok=True)
    self.data: dict[int, self.lmi] = {}

    self.__load()

  def __load(self) -> None:
    try:
      with open(self.file_path, 'r', encoding='utf-8') as f:
        self.data = decode_io(f)
    except FileNotFoundError:
      pass

  def __save(self) -> None: # pylint: disable=unused-private-member
    with open(self.file_path, 'w', encoding='utf-8') as f:
      encode_io(self.data, f)


class UsefulClient(commands.AutoShardedBot):
  """
  ## Description
  The client class for the bot.
  """
  MAX_LVL = 100

  def __init__(self, prefix: str = '!', invite: str = None, **options):
    init_logger()
    intents = discord.Intents.all()
    self.__started_once = False
    self.__invite = invite
    self.__start_time = datetime.datetime.now()
    super().__init__(command_prefix=prefix, intents=intents, **options)

    self.__db = UsefulDatabase()
    self.__dispatcher: MessageSender = MessageSender()
    self.__embed_builder: Embedder = Embedder()

    self.log = logging.getLogger('resistance.client')

  @property
  def invite(self) -> str:
    return self.__invite

  @property
  def uptime(self) -> str:
    return str(datetime.datetime.now() - self.__start_time).split('.', maxsplit=1)[0]

  @property
  def start_time(self) -> float:
    return self.__start_time.timestamp()

  @property
  def dispatcher(self) -> MessageSender:
    return self.__dispatcher

  @property
  def embed_builder(self) -> Embedder:
    return self.__embed_builder

  @override
  async def on_ready(self):
    await self.tree.sync()
    await self.change_presence(
      status=discord.Status.online,
      activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f'/help (v{__version__})',
      ),
    )

    if not self.__started_once:
      TaskManager(self, self.__db, self.dispatcher, self.embed_builder).run.start() # pylint: disable=no-member
      self.log.info('Logged in as %s (ID: %d)', self.user, self.user.id)
      self.log.info('Connected to %d guilds', len(self.guilds))

      self.__started_once = True

    else:
      self.log.info('Skipping dupplicate on_ready event')

  @override
  async def setup_hook(self):
    await self.setup()

    self.log.info('Messing around ...')

    self.__db.test()
    self.__db.connect()

    signal.signal(signal.SIGINT, self.on_end)
    signal.signal(signal.SIGTERM, self.on_end)

    self.log.info('Ready to connect 🥳 !')

  @override
  def run(self, token: str) -> None:
    """
    Runs the bot.

    ## Parameters
    ```py
    >>> token : str
    ```
    The bot token.
    """
    super().run(token=token, log_handler=None)

  async def on_app_command_error(self, interaction: discord.Interaction, error: Exception):
    """ Handles errors from slash commands. """
    embed: discord.Embed = None
    match error:
      case commands.MissingRequiredArgument:
        embed = self.embed_builder.build_error_embed(
          title='Missing argument !',
          description=f'{FAIL_EMOJI} You need to specify the `{error.param.name}` argument.',
        )
      case commands.BadArgument:
        embed = self.embed_builder.build_error_embed(
          title='Bad argument !',
          description=f'{FAIL_EMOJI} You need to specify a valid `{error.param.name}` argument.',
        )
      case _:
        embed = self.embed_builder.build_error_embed(
          title='Oopsie, something went wrong !',
          description=
          f'{FAIL_EMOJI} Please let an admin know about this issue : \n```py\n{error.with_traceback(None)}\n```',
        )
    if not embed:
      self.log.critical('Panic while handling slash command unhandled exception: embed is empty')
      sys.exit(1)

    try:
      await self.dispatcher.reply_with_embed(interaction, embed)

    except Exception as e: # pylint: disable=broad-except

      self.log.critical('Panic while sending slash command unhandled exception: %s\n\n%s\n%s', e, embed.title,
                        embed.description)

  def on_end(self, sig: int, _: Any) -> None:
    """
    Synchronously shuts down the bot.

    ## Parameters
    ```py
    >>> sig : int
    ```
    The signal number.
    ```py
    >>> frame : Frame
    ```
    The frame object.
    """
    print('', end='\r')
    self.log.warning('Received signal %s, shutting down...', signal.Signals(sig).name)
    self.log.info('Shutting down...')
    self.__db.disconnect()
    self.log.info('Shutdown complete')
    sys.exit(0)

  async def setup(self):
    self.log.info('Setting up...')

    await self.add_cog(Sudo(self))
    await self.add_cog(BotLog(self))

    await self.add_cog(Poll(self))

    await self.add_cog(Utils(self))
    await self.add_cog(Xp(self, self.__db))

    self.log.info('Setting up complete')

  @staticmethod
  @lru_cache(maxsize=None)
  def lvl_to_xp(lvl: int) -> int:
    """Converts a level to xp."""
    return int(1.6412*lvl*lvl*lvl + 23.441*lvl*lvl + 67.981*lvl)

  def xp_to_lvl(self, xp: int) -> int:
    """Converts xp to a level."""
    if xp < 0:
      return 0

    if xp < UsefulClient.lvl_to_xp(1):
      return 0
    for i in range(1, UsefulClient.MAX_LVL):
      if UsefulClient.lvl_to_xp(i) <= xp < UsefulClient.lvl_to_xp(i + 1):
        return i
    self.log.warning('Maximum level hit with %d xp', xp)
    return UsefulClient.MAX_LVL

  @staticmethod
  def xp_from_msg_len(msg_len: int) -> int:
    return round(math.log10(msg_len + 1) * 10)

  def xp_from_message(self, message: Message) -> int:
    xp_to_add = UsefulClient.xp_from_msg_len(len(message.content)) +\
                5 * len(message.attachments) +\
                2 * len(message.stickers)
    # todo: scale down based on how much the user spams

    return xp_to_add

  @override
  async def on_message(self, message: Message, /):
    if message.channel.type is discord.ChannelType.private:
      return
    return # todo: remove this line to enable xp and event dispatching

    # pylint: disable=unreachable
    if message.author.bot:
      return await self.process_cmd(message)
    await self.process_msg(message)

  async def process_msg(self, message: Message):
    self.__db.create_user(message.author.id, message.author.name)
    old_xp = self.__db.add_xp_to_user(message.author.id, xp_added := self.xp_from_message(message))
    new_xp = old_xp + xp_added
    old_lvl, new_lvl = self.xp_to_lvl(old_xp), self.xp_to_lvl(new_xp) # pylint: disable=unused-variable
                                                                      # todo: lvl up event

  async def process_cmd(self, message: Message): # pylint: disable=unused-argument
    ...

  async def dispatch_reactions(self, message: Message): # pylint: disable=unused-argument
    ...

  async def do_auto_responses(self, message: Message): # pylint: disable=unused-argument
    ...
