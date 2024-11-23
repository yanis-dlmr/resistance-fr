from typing import Any

import discord
from discord import app_commands
from discord.ext import commands
import datetime

from ..db import *
from ..helper import *
from ..messages.timestamp import *

__all__ = ['Events']


week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


@app_commands.default_permissions(manage_guild=True)
class Events(UsefullCog):
  
  def __init__(self, client: commands.AutoShardedBot, db: UsefulDatabase):
    self.__db = db
    super().__init__(client)
    
  def schedule_dict_to_string(self, schedule: dict[str, Any]) -> str:
    """
    Convert a schedule dictionary to a string with the format:
    ```
    {
      'day': 'Monday',
      'time': '12:00',
    }
    ```
    """
    week_day_index = schedule['day'] # 0 = Monday, 6 = Sunday
    time = schedule['time']
    if week_day_index == 69:
      return f'Everyday at `{time}`'
    return f'On {week_days[week_day_index]} at `{time}`'

  def __reload_config(self) -> None:
    """
    Reload the config
    """
    self.__config = list(self.__db.get_config())[0]


  def get_next_timestamp(self, schedule: dict[str, Any]) -> int:
    """
    Get the next timestamp for a schedule.
    Schedule is a dictionary with the format:
    ```
    {
      'day': 0, # 0 = Monday, 6 = Sunday
      'time': '12:00',
    }
    ```
    """
    week_day_index = schedule['day']
    time = schedule['time']
    now = datetime.datetime.now()
    today = now.weekday()
    if week_day_index == 69:
      return now.replace(hour=int(time.split(':')[0]), minute=int(time.split(':')[1]), second=0, microsecond=0).timestamp()
    if today < week_day_index:
      next_day = week_day_index
    elif today == week_day_index:
      next_day = week_day_index
      if now.strftime('%H:%M') < time:
        return now.timestamp()
    else:
      next_day = week_day_index + 7
    next_day = now + datetime.timedelta(days=next_day - today)
    next_day = next_day.replace(hour=int(time.split(':')[0]), minute=int(time.split(':')[1]), second=0, microsecond=0)
    return next_day.timestamp()

  @app_commands.command(name='help', description='Get help about a command')
  async def help(self, interaction: discord.Interaction):
    embed = self.embed_builder.build_help_embed(
      title='Help for `Events` group',
      description='`Events` group contains commands that are useful for developers and users.',
    ).add_field(
      name='🧾 `display`',
      value='Test a specific event name to see how it would look like.',
      inline=False,
    ).add_field(
      name='📅 `list-tasks`',
      value='Lists all tasks events available on the server.',
      inline=False,
    ).add_field(
      name='📅 `list-on-message`',
      value='Lists all on message events available on the server.',
      inline=False,
    ).add_field(
      name='📅 `list-on-edit`',
      value='Lists all on edit events available on the server.',
      inline=False,
    ).add_field(
      name='📣 `trigger-routine`',
      value='Trigger a routing by giving the related on-message `event_name` (send the related `keyword`).',
      inline=False,
    )
    await self.dispatcher.reply_with_embed(interaction, embed)
    self.log_interaction(interaction)

  @app_commands.command(name='display', description='Test a specific event name to see how it would look like 🧾')
  async def display(self, interaction: discord.Interaction, event_name: str):
    embeds: list[discord.Embed] = []
    content: str = ''
    self.__reload_config()
    
    for event in self.__db.get_events():
      if event['event_name'] == event_name:
        role_name = event['role_name']
        content = f'<@&{self.__config["role_id"][role_name]}> {event["content"]}'
        embeds.append(self.embed_builder.build_event_embed(**event['embed']))
        
    for event in self.__db.get_on_message_events():
      if event['event_name'] == event_name:
        role_name = event['role_name']
        content = f'<@&{self.__config["role_id"][role_name]}> {event["content"]}'
        embeds.append(self.embed_builder.build_event_embed(**event['embed']))
        
    for event in self.__db.get_on_edit_events():
      if event['event_name'] == event_name:
        role_name = event['role_name']
        content = f'<@&{self.__config["role_id"][role_name]}> {event["content"]}'
        embeds.append(self.embed_builder.build_event_embed(**event['embed']))
        
    if len(embeds) > 0:
      await self.dispatcher.reply_with_multiple_embeds(interaction, embeds, content)
      self.log_interaction(interaction)
    else:
      embed = self.embed_builder.build_error_embed(
        title='Event not found !',
        description=f'{FAIL_EMOJI} The event with event name `{event_name}` does not exist.',
      )
      await self.dispatcher.reply_with_embed(interaction, embed)
      self.log_interaction(interaction)
  
  @app_commands.command(name='list-tasks', description='Lists all tasks events available on the server 📅')
  async def list_tasks(self, interaction: discord.Interaction):
    events = self.__db.get_events()
    embed = self.embed_builder.build_help_embed(
      title='Tasks events list',
      description='Here are all the tasks events available on the server.',
    )
    for event in events:
      event_name = event['event_name']
      channel_name = event['channel_name']
      role_name = event['role_name']
      self.__reload_config()
      channel_id = self.__config['channel_id'][channel_name]
      role_id = self.__config['role_id'][role_name]
      channel = self.client.get_channel(channel_id)
      role = channel.guild.get_role(role_id)
      state = 'Enable' if event['state'] else 'Disable'
      value = f"> - Channel `{channel_name}`: {channel.mention}\n> - Role `{role_name}`: {role.mention}\n> - State: `{state}`\n> - Schedule:\n"
      for schedule in event['schedule']:
        next_timestamp = self.get_next_timestamp(schedule)
        value += f">   - {self.schedule_dict_to_string(schedule)}. Next {format_timestamp(next_timestamp, TimestampType.RELATIVE)}\n"
      embed.add_field(
        name=f'`{event_name}` event:',
        value=value,
        inline=False,
      )
    await self.dispatcher.reply_with_embed(interaction, embed)
    self.log_interaction(interaction)
    
  @app_commands.command(name='list-on-message', description='Lists all on message events available on the server 📅')
  async def list_on_message(self, interaction: discord.Interaction):
    events = self.__db.get_on_message_events()
    embed = self.embed_builder.build_help_embed(
      title='On message events list',
      description='Here are all the on message events available on the server.',
    )
    for event in events:
      event_name = event['event_name']
      channel_name = event['channel_name']
      role_name = event['role_name']
      self.__reload_config()
      channel_id = self.__config['channel_id'][channel_name]
      role_id = self.__config['role_id'][role_name]
      channel = self.client.get_channel(channel_id)
      role = channel.guild.get_role(role_id)
      state = 'Enable' if event['state'] else 'Disable'
      value = f"> - Channel `{channel_name}`: {channel.mention}\n> - Role `{role_name}`: {role.mention}\n> - State: `{state}`\n> - Keywords: `{', '.join(event['keywords'])}`\n"
      embed.add_field(
        name=f'`{event_name}` event:',
        value=value,
        inline=False,
      )
    await self.dispatcher.reply_with_embed(interaction, embed)
    self.log_interaction(interaction)
    
  @app_commands.command(name='list-on-edit', description='Lists all on edit events available on the server 📅')
  async def list_on_edit(self, interaction: discord.Interaction):
    events = self.__db.get_on_edit_events()
    embed = self.embed_builder.build_help_embed(
      title='On edit events list',
      description='Here are all the on edit events available on the server.',
    )
    for event in events:
      event_name = event['event_name']
      content = event['content']
      channel_name = event['channel_name']
      role_name = event['role_name']
      self.__reload_config()
      channel_id = self.__config['channel_id'][channel_name]
      role_id = self.__config['role_id'][role_name]
      channel = self.client.get_channel(channel_id)
      role = channel.guild.get_role(role_id)
      state = 'Enable' if event['state'] else 'Disable'
      value = f"> - Channel `{channel_name}`: {channel.mention}\n> - Role `{role_name}`: {role.mention} {content}\n> - State: `{state}`\n> - Keywords: `{', '.join(event['keywords'])}`\n"
      embed.add_field(
        name=f'`{event_name}` event:',
        value=value,
        inline=False,
      )
    await self.dispatcher.reply_with_embed(interaction, embed)
    self.log_interaction(interaction)
    
  @app_commands.command(name='trigger-routine', description='Trigger a routing by giving the related on-message `event_name` (send the related `keyword`).')
  async def trigger_routine(self, interaction: discord.Interaction, event_name: str):
    self.__reload_config()
    for event in self.__db.get_on_message_events():
      if event['event_name'] == event_name:
        keywords = event['keywords']
        for channel_id in self.__config['event_tracker']['channel_id']:
          channel = self.client.get_channel(channel_id)
          await channel.send(keywords[0])
          embed = self.embed_builder.build_success_embed(
            title='Routine triggered !',
            description=f'{SUCCESS_EMOJI} The routine called `{event_name}` has been triggered in channel {channel.mention} by sending the keyword `{keywords[0]}`.',
          )
          await self.dispatcher.reply_with_embed(interaction, embed)
          self.log_interaction(interaction)
          return
    embed = self.embed_builder.build_error_embed(
      title='Event not found !',
      description=f'{FAIL_EMOJI} The event with event name `{event_name}` does not exist.',
    )
    await self.dispatcher.reply_with_embed(interaction, embed)
    self.log_interaction(interaction)