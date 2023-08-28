import datetime
import time
from typing import Any

import logging
from discord.ext import commands, tasks

from ..db import *
from ..messages import MessageSender, Embedder

__all__ = ['TaskManager']


def fiveteen_minutes_earlier(timestr: str) -> str:
  # time is in format HH:MM
  h, m = timestr.split(':')
  t = datetime.time(hour=int(h), minute=int(m))
  r = (datetime.datetime.combine(datetime.date.today(), t) - datetime.timedelta(minutes=15)).time()
  return r.strftime('%02H:%02M')


class TaskManager:
  """
  Manage a loop event that runs Tasks imported from the database at every interval.
  """

  def __init__(
    self,
    client: commands.AutoShardedBot,
    db: UsefulDatabase,
    dispatcher: MessageSender,
    embed_builder: Embedder,
  ):
    self.__config: dict[str, dict] = {}
    # config['tasks'] = {}
    # config['language'] = None

    self.dispatcher: MessageSender = dispatcher
    self.embed_builder: Embedder = embed_builder

    self.log = logging.getLogger('resistance.tasks')
    self.client = client
    self.__db = db

  def __reload_config(self) -> None:
    """
    Reload the config
    """
    self.__config = list(self.__db.get_config())[0]

  @tasks.loop(minutes=1.0)
  async def run(self) -> None:
    """
    Run the tasks
    """
    for event in self.__db.get_events():
      if self.__valid(event):
        self.__reload_config()
        await self.__send(event)

  def __valid(self, event: dict[str, Any]) -> bool:
    """
    Check if the event is valid
    """
    return self.__valid_state(event) and self.__valid_time(event)

  def __valid_state(self, event: dict[str, Any]) -> bool:
    """
    Check if the event is enabled
    """
    return event['state']

  def __valid_time(self, event: dict[str, Any]) -> bool:
    """
    Check if the event is matched with the current time
    """
    now = time.gmtime(time.time() + 3600)       # utc + 1
    day = now.tm_wday
    hour = now.tm_hour
    minute = now.tm_min
    current_time = '%02d:%02d' % (hour, minute) # pylint: disable=consider-using-f-string

    schedule = event['schedule']
    for s in schedule:
      if s['day'] == day or s['day'] == 69:
        if fiveteen_minutes_earlier(s['time']) == current_time:
          return True
    return False

  async def __send(self, event: dict[str, Any]) -> None:
    """
    Send the event
    """
    tag = event['tag']
    channel_id = self.__config['tag_id'][tag]['channel_id']
    channel = self.client.get_channel(channel_id)
    embed = self.__build_embed(event)
    content = f'<@&{self.__config["tag_id"][tag]["role_id"]}> {event["content"]}'
    await self.dispatcher.send_channel_event(channel, embed, content)
    self.log.debug('Dispatched event \'%s\' to channel %s', tag, channel_id)

  def __build_embed(self, event: dict[str, Any]) -> None:
    """
    Build the embed
    """
    return self.embed_builder.build_event_embed(**event['embed'])
