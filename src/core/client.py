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

# from .bot_events import *

from .bot_events import LvlUpEvent
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
      self.log.info('🔗 Logged in as %s (ID: %d)', self.user, self.user.id)
      self.log.info('🔗 Connected to %d guilds', len(self.guilds))

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
    self.log.warning('⚰️ Received signal %s, shutting down...', signal.Signals(sig).name)
    self.log.info('⚰️ Shutting down...')
    self.__db.disconnect()
    self.log.info('⚰️ Shutdown complete')
    sys.exit(0)

  async def setup(self):
    self.log.info('Setting up...')

    await self.add_cog(Sudo(self))
    await self.add_cog(BotLog(self))
    await self.add_cog(Config(self, self.__db))
    
    await self.add_cog(Poll(self))

    await self.add_cog(Utils(self))
    await self.add_cog(Xp(self, self.__db))
    await self.add_cog(Events(self, self.__db))

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
    # return # todo: remove this line to enable xp and event dispatching

    # pylint: disable=unreachable
    if message.author.bot:
      bot_on_message_events = BotOnMessageEvents(self, self.__db)
      await bot_on_message_events.process_msg(message)
      return
    
    return # todo: remove this line to enable xp
    await self.process_msg(message)

  async def process_msg(self, message: Message):
    user_id = message.author.id
    self.__db.create_user(user_id, message.author.name)
    old_xp = self.__db.add_xp_to_user(user_id, xp_added := self.xp_from_message(message))
    new_xp = old_xp + xp_added
    old_lvl, new_lvl = self.xp_to_lvl(old_xp), self.xp_to_lvl(new_xp) # pylint: disable=unused-variable
    if old_lvl < new_lvl:
      await LvlUpEvent(self.__db, message.author, new_lvl).build_event()
    
  async def dispatch_reactions(self, message: Message): # pylint: disable=unused-argument
    ...

  async def do_auto_responses(self, message: Message): # pylint: disable=unused-argument
    ...
    
  @override
  async def on_message_edit(self, before: Message, after: Message):
    if before.author.bot:
      await BotOnEditEvents(self, self.__db).process_msg(after)


class BotOnMessageEvents(UsefullCog):
  
  def __init__(self, client: UsefulClient, db: UsefulDatabase):
    self.__db = db
    super().__init__(client)
    

  def __reload_config(self) -> None:
    """
    Reload the config
    """
    self.__config = list(self.__db.get_config())[0]
    
  async def process_msg(self, message: Message):
    self.__reload_config()
    if self.__valid_cmd_on_message(message):
      on_message_events = self.__db.get_on_message_events()
      for on_message_event in on_message_events:
        if self.__valid(on_message_event, message):
          await self.__send(on_message_event)
          self.__activate_corresponding_task(on_message_event)
  
  def __activate_corresponding_task(self, on_message_event: dict[str, Any]) -> None:
    """
    Activate the corresponding task
    """
    tasks_events = self.__db.get_events()
    for task_event in tasks_events:
      if self.__corresponding_task(task_event, on_message_event):
        self.__db.activate_task(task_event)
        self.log.info('Activated task \'%s\'', task_event['event_name'])
          
  def __valid_cmd_on_message(self, message: Message) -> bool:
    """
    Check if the message came from a valid bot and if came from a valid channel 
    """
    return message.author.id in self.__config['event_tracker']['bot_id'] and message.channel.id in self.__config['event_tracker']['channel_id']
  
  def __valid(self, event: dict[str, Any], message: Message) -> bool:
    """
    Check if the event is valid
    """
    return self.__valid_state(event) and self.__valid_keywords(event, message)
  
  def __valid_state(self, event: dict[str, Any]) -> bool:
    """
    Check if the event is enabled
    """
    return event['state']
  
  def __valid_keywords(self, event: dict[str, Any], message: Message) -> bool:
    """
    Check if the event is matched with the current time
    """
    keywords = event['keywords']
    for keyword in keywords:
      if keyword in message.content:
        return True
    return False
  
  async def __send(self, event: dict[str, Any]) -> None:
    """
    Send the event
    """
    event_name = event['event_name']
    channel_name = event['channel_name']
    role_name = event['role_name']
    # channel_id = self.__config['channel_id'][channel_name]
    channel_id = 1000506839319969942 # todo : remove this line a uncomment the previous one
    channel = self.client.get_channel(channel_id)
    embed = self.__build_embed(event)
    content = f'<@&{self.__config["role_id"][role_name]}> {event["content"]}'
    await self.dispatcher.send_channel_event(channel, embed, content)
    self.log.info('Dispatched on_message event \'%s\' to channel %s', event_name, channel_id)

  def __build_embed(self, event: dict[str, Any]) -> discord.Embed:
    """
    Build the embed
    """
    return self.embed_builder.build_event_embed(**event['embed'])
  
  def __corresponding_task(self, task_event: dict[str, Any], on_message_event: dict[str, Any]) -> bool:
    """
		Check if the event is matched with the current time
    """
    return task_event['event_name'] == on_message_event['event_name']


class BotOnEditEvents(UsefullCog):
  
  def __init__(self, client: UsefulClient, db: UsefulDatabase):
    self.__db = db
    super().__init__(client)
    

  def __reload_config(self) -> None:
    """
    Reload the config
    """
    self.__config = list(self.__db.get_config())[0]
    
  async def process_msg(self, message: Message):
    self.__reload_config()
    if self.__valid_cmd_on_message(message):
      events = self.__db.get_on_edit_events()
      for event in events:
        if self.__valid(event, message):
          await self.__send(event)
          
  def __valid_cmd_on_message(self, message: Message) -> bool:
    """
    Check if the message came from a valid bot and if came from a valid channel 
    """
    return message.author.id in self.__config['event_tracker']['bot_id'] and message.channel.id in self.__config['event_tracker']['channel_id']
  
  def __valid(self, event: dict[str, Any], message: Message) -> bool:
    """
    Check if the event is valid
    """
    return self.__valid_state(event) and self.__valid_keywords(event, message)
  
  def __valid_state(self, event: dict[str, Any]) -> bool:
    """
    Check if the event is enabled
    """
    return event['state']
  
  def __valid_keywords(self, event: dict[str, Any], message: Message) -> bool:
    """
    Check if the event is matched with the current time
    """
    keywords = event['keywords']
    for keyword in keywords:
      if keyword in message.content:
        return True
    return False
  
  async def __send(self, event: dict[str, Any]) -> None:
    """
    Send the event
    """
    event_name = event['event_name']
    channel_name = event['channel_name']
    role_name = event['role_name']
    # channel_id = self.__config['channel_id'][channel_name]
    channel_id = 1000506839319969942 # todo : remove this line a uncomment the previous one
    channel = self.client.get_channel(channel_id)
    embed = self.__build_embed(event)
    content = f'<@&{self.__config["role_id"][role_name]}> {event["content"]}'
    await self.dispatcher.send_channel_event(channel, embed, content)
    self.log.info('Dispatched on_message event \'%s\' to channel %s', event_name, channel_id)

  def __build_embed(self, event: dict[str, Any]) -> discord.Embed:
    """
    Build the embed
    """
    return self.embed_builder.build_event_embed(**event['embed'])