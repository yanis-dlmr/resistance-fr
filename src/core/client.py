import os
import signal
import sys

import discord
from discord.ext.commands import errors
from discord.ext.commands.context import Context
import jellyfish

from typing import Any, Callable
from typing_extensions import override
from discord.ext import commands
from discord.message import Message
from tokenize import tokenize
from io import StringIO

import datetime
import math
from threading import Timer

from ..helper import *
from ..helper import logger
from ..helper.logger import logger as log
from ..commands import *
from ..db import *

from ..version import __version__

__all__ = ['UsefulClient']


class RepeatedTimer:
  """"
  A timer that repeats itself.

  ## Example
  ```py
  from time import sleep

  def hello(name: str):
    print(f"Hello, {name}!")

  print "starting..."
  rt = RepeatedTimer(1, hello, "World") # it auto-starts, no need of rt.start()
  try:
    sleep(5) # your long-running job goes here...
  finally:
    rt.stop() # better in a try/finally block to make sure the program ends!
  ```
  """

  def __init__(
    self,
    interval: float,
    function: Callable,
    *args: Any,
    **kwargs: Any,
  ) -> None:
    """
    New RepeatedTimer.

    ## Parameters
    ```py
    >>> interval: float
    ```
    The interval in seconds between each call of the function.
    ```py
    >>> function: Callable
    ```
    The function to call.
    ```py
    >>> *args: Any, **kwargs: Any
    ```
    The arguments to pass to the function.
    """
    self.__timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.__timer = Timer(self.interval, self._run)
      self.__timer.start()
      self.is_running = True

  def stop(self):
    self.__timer.cancel()
    self.is_running = False


class UsefulClient(commands.AutoShardedBot):
  """
  ## Description
  The client class for the bot.
  """
  MAX_LVL = 100

  def __init__(self, prefix: str = '!', invite: str = None, **options):
    intents = discord.Intents.all()
    self.__invite = invite
    self.__start_time = datetime.datetime.now()
    super().__init__(command_prefix=prefix, intents=intents, **options)

    self.__db = UsefulDatabase()

  @property
  def invite(self) -> str:
    return self.__invite

  @property
  def uptime(self) -> str:
    return str(datetime.datetime.now() - self.__start_time).split('.')[0]

  @property
  def start_time(self) -> float:
    return self.__start_time.timestamp()

  @override
  async def on_ready(self):
    log.info(f'Logged in as {self.user} (ID: {self.user.id})')
    log.info(f'Connected to {len(self.guilds)} guilds')
    await self.setup()

    log.info('Messing around ...')
    await self.tree.sync()
    await self.change_presence(
      status=discord.Status.online,
      activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f'v {__version__}',
      ),
    )
    self.__db.test()
    self.__db.connect()

    signal.signal(signal.SIGINT, self.on_end_handler)
    signal.signal(signal.SIGTERM, self.on_end_handler)

    log.info('Ready 🥳 !')

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
    super().run(
      token,
      reconnect=True,
      log_handler=logger.console_handler,
      log_formatter=logger.default_formatter,
      log_level=logger.log_lvl,
    )

  def on_end_handler(self, sig: int, frame) -> None: # pylint: disable=unused-argument
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
    log.info('Shutting down...')
    self.__db.disconnect()
    log.info('Shutdown complete')
    sys.exit(0)

  async def setup(self):
    log.info('Setting up...')

    await self.add_cog(Sudo(self))
    await self.add_cog(BotLog(self))

    await self.add_cog(Poll(self))

    await self.add_cog(Utils(self))
    await self.add_cog(Xp(self, self.__db))

    log.info('Setting up complete')

  @staticmethod
  def lvl_to_xp(lvl: int) -> int:
    """Converts a level to xp."""
    return int(1.6412*lvl*lvl*lvl + 23.441*lvl*lvl + 67.981*lvl)

  @staticmethod
  def xp_to_lvl(xp: int) -> int:
    """Converts xp to a level."""
    if xp < 0:
      return 0

    if xp < UsefulClient.lvl_to_xp(1):
      return 0
    for i in range(1, UsefulClient.MAX_LVL):
      if UsefulClient.lvl_to_xp(i) <= xp < UsefulClient.lvl_to_xp(i + 1):
        return i
    return UsefulClient.MAX_LVL

  @staticmethod
  def xp_from_msg_len(msg_len: int) -> int:
    return round(math.log10(msg_len + 1) * 10)

  @staticmethod
  def xp_from_additionnal_attatchements(attachments: int) -> int:
    return 5 * attachments

  @staticmethod
  def xp_from_message(message: Message) -> int:
    return UsefulClient.xp_from_msg_len(len(message.content)) +\
           UsefulClient.xp_from_additionnal_attatchements(len(message.attachments))

  @override
  async def on_message(self, message: Message):
    if message.author.bot:
      await self.process_cmd(message)
    await self.process_msg(message)

  async def process_msg(self, message: Message):
    ...

  async def process_cmd(self, message: Message):
    ...
