from dataclasses import dataclass

import discord
from discord.ext import commands, tasks

import time

from ..db import *
from ..messages import MessageSender, Embedder

__all__ = ['TaskManager']

@dataclass
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
        embed: discord.Embed,
    ):
        self.__config: dict[str, dict] = {}
        # config['tasks'] = {}
        # config['language'] = None
        self.__events: list
        
        self.dispatcher: MessageSender = dispatcher
        self.embed_builder: Embedder = embed_builder
        self.embed = embed
        
        self.client = client
        self.__db = db
        
        self.__setup()
    
    def __setup(self) -> None:
        """
        Connect to the db and load the config
        """
        self.__config = self.__db.get_config()
    
    @tasks.loop(minutes=1.0)
    async def run(self) -> None:
        """
        Run the tasks
        """
        self.__events = self.__db.get_events()
        for event in self.__events:
            if self.__valid(event):
                await self.__send(event)
    
    def __valid(self, event: dict) -> bool:
        """
        Check if the event is valid
        """
        return (self.__valid_state(event) and self.__valid_time(event))

    def __valid_state(self, event: dict) -> bool:
        """
        Check if the event is enabled
        """
        return event['state']
    
    def __valid_time(self, event: dict) -> bool:
        """
        Check if the event is matched with the current time
        """
        now = time.gmtime(time.time() + 3600) # UTC+1 time
        day = now.tm_wday
        hour = now.tm_hour
        minute = now.tm_min
        current_time = f"{hour}:{minute}"
        
        schedule = event['schedule']
        for i in range(schedule):
            if schedule[i][0] == day or schedule[i][0] == 69:
                if schedule[i][1] == current_time:
                    return True
    
    async def __send(self, event: dict) -> None:
        """
        Send the event
        """
        tag = event['tag']
        channel_id = self.__config["tasks"][tag][channel_id]
        channel = self.client.get_channel(channel_id)
        self.__build_embed(event)
        await self.dispatcher.send_channel_embed(channel, self.embed)
    
    def __build_embed(self, event: dict) -> None:
        """
        Build the embed
        """
        language_value = self.__config["language"]
        self.embed = self.embed_builder.build_embed(
            title=event['title'][language_value],
            description=event['description'][language_value],
            colour=discord.Colour.blurple(),
            footer=None,
            footer_icon=None,
            thumbnail=event['thumbnail'],
            image=event['picture'],
        )