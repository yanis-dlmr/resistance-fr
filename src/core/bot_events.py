from typing import Any

from discord import User, File, Embed
from discord.ext import commands

from ..db import *
from ..helper import UserBanner

from ..messages import MessageSender, Embedder


__all__ = ['LvlUpEvent', 'WelcomeEvent']


class UsefulEvent:
  """
  Class used by LvlUpEvent and WelcomeEvent to inherit from.
  """
  
  def __init__(self, db: UsefulDatabase, user: User) -> None:
    """
    Initialize UsefulEvent class with the database and user object.
    
    ## Parameters
    ```py
    >>> db : UsefulDatabase
    ```
    Database object.
    ```py
    >>> user : discord.User
    ```
    User object.
    """
    self.__config = list(db.get_config())[0]
    self.__user = user
    self.__sender = MessageSender()
    self.__embed_builder = Embedder()
    
    self.__init_available_vars()
    
  def __init_available_vars(self) -> None:
    """
    Initialize available variables.
    """
    self.properties = {
      'user_name': self.user.name,
      'user_mention': self.user.mention,
    }
  
  def add_available_vars(self, **kwargs) -> None:
    """
    Add available variables.
    
    ## Parameters
    ```py
    >>> kwargs : dict
    ```
    Variables to add.
    """
    self.properties.update(kwargs)
  
  @property
  def config(self) -> dict:
    return self.__config
  
  @property
  def user(self) -> User:
    return self.__user
  
  @property
  def sender(self) -> MessageSender:
    return self.__sender
  
  @property
  def embed_builder(self) -> Embedder:
    return self.__embed_builder

  def set_event_config(self, event_config: dict[str, Any]) -> None:
    """
    Set the event config.
    
    ## Parameters
    ```py
    >>> event_config : dict[str, Any]
    ```
    Event config.
    """
    self.event_config = event_config

  def build_embed(self, embed: dict[str, Any]) -> Embed:
    """
    Build the embed
    """
    embed = self.replace_dict_vars(embed)
    embed = self.embed_builder.build_event_embed(**embed)
    embed.set_image(url="attachment://banane.png")
    
    return embed

  def build_content(self, content: str) -> str:
    """
    Build the content.
    
    ## Parameters
    ```py
    >>> content : str
    ```
    Content.
    
    ## Returns
    ```py
    >>> str
    ```
    Content.
    """
    return self.replace_vars(content)
  
  def replace_dict_vars(self, embed: dict[str, Any]) -> dict[str, Any]:
    """
    Replace the variables in the dictionary.
    
    ## Parameters
    ```py
    >>> embed : dict[str, Any]
    ```
    Dictionary.
    
    ## Returns
    ```py
    >>> dict[str, Any]
    ```
    Dictionary with replaced variables.
    """
    return {k: self.replace_vars(v) for k, v in embed.items()}
  
  def replace_vars(self, content: str) -> str:
    """
    Replace the variables in the content.
    
    ## Parameters
    ```py
    >>> content : str
    ```
    Content.
    
    ## Returns
    ```py
    >>> str
    ```
    Content with replaced variables.
    """
    return content.format(**self.properties)
  
  def build_event(self) -> tuple[str, Embed, File]:
    """
    Build the content: message, embed and user_banner for the event.
    
    ## Returns
    ```py
    >>> tuple[str, discord.Embed, discord.File]
    ```
    Content, embed and user banner.
    """
    return (self.build_content(self.event_config['content']),
            self.build_embed(self.event_config['embed']),
            UserBanner(self.config['background_urls'], self.config['server_name']).get_banner(self.user.avatar))


class LvlUpEvent(UsefulEvent, commands.AutoShardedBot):
  """
  Initialize LvlUpEvent class with the database, user object, and next level.

  ## Parameters
  ```py
  >>> db : UsefulDatabase
  ```
  Database object.
  ```py
  >>> user : discord.User
  ```
  User object.
  ```py
  >>> next_lvl : int
  ```
  Next level.
  """
  
  def __init__(self, db: UsefulDatabase, user: User, next_lvl: int) -> None:
    super().__init__(db, user)
    self.add_available_vars(next_lvl=next_lvl)
    self.set_event_config(self.config['level_up_event'])
    
  async def send_level_up(self) -> None:
    """
    Send the level up event to the lvl up channel.
    """
    # channel = self.get_channel(self.config['channel_id']['level_up'])
    channel = self.get_channel(1000506839319969942) # todo : remove this line a uncomment the previous one
    content, embed, user_banner = self.build_event()
    await self.sender.send_lvl_up_event(channel, content, embed, user_banner)
    self.log.info('Dispatched level up event')
  

class WelcomeEvent(UsefulEvent, commands.AutoShardedBot):
  """
  Initialize WelcomeEvent class with the database and user object.

  ## Parameters
  ```py
  >>> db : UsefulDatabase
  ```
  Database object.
  ```py
  >>> user : discord.User
  ```
  User object.
  """
  
  def __init__(self, db: UsefulDatabase, user: User) -> None:
    super().__init__(db, user)
    self.set_event_config(self.config['welcome_event'])
    
  async def send_welcome(self) -> None:
    """
    Send the welcome event to the welcome channel.
    """
    # channel = self.get_channel(self.config['channel_id']['welcome'])
    channel = self.get_channel(1000506839319969942) # todo : remove this line a uncomment the previous one
    content, embed, user_banner = self.build_event()
    await self.sender.send_welcome_event(channel, content, embed, user_banner)
    self.log.info('Dispatched welcome event')