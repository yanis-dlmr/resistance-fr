from collections.abc import Coroutine
from typing import Any

from arrow import Arrow
import discord

from .timestamp import *

__all__ = [
  'reply_with_embed',
  'edit_reply_with_embed',
  'reply_with_status_embed',
  'send_status_embed',
  'send_poll_embed',
  'send_channel_message',
  'send_channel_file',
  'send_poll_followup_embed',
  'send_xp_embed',
]


#%% base functions
def send_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
  ephemeral: bool = False,
  delete_after: float = None,
):
  return interaction.response.send_message(embed=embed, ephemeral=ephemeral, delete_after=delete_after)


def edit_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
):
  return interaction.edit_original_response(embed=embed)


#%% custom functions


def reply_with_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
) -> Coroutine[Any, Any, None]:
  """
  reply the sender with an embed

  ## Parameters
  ```py
  >>> interaction : discord.Interaction
  ```
  original interaction
  ```py
  >>> embed : discord.Embed
  ```
  embed to send

  ## Returns
  ```py
  Coroutine[Any, Any, None] : the coroutine that sends the embed
  ```
  """
  return send_embed(interaction, embed)


def edit_reply_with_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
) -> Coroutine[Any, Any, None]:
  """
  edit the reply with an embed

  ## Parameters
  ```py
  >>> interaction : discord.Interaction
  ```
  original interaction
  ```py
  >>> embed : discord.Embed
  ```
  embed to send

  ## Returns
  ```py
  Coroutine[Any, Any, None] : the coroutine that sends the embed
  ```
  """
  return edit_embed(interaction, embed)


def reply_with_status_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
  failed: bool = False,
) -> Coroutine[Any, Any, None]:
  """
  reply the sender with a status embed\\
  will automatically delete the embed after 5 seconds and add a timestamp to the description

  ## Parameters
  ```py
  >>> interaction : discord.Interaction
  ```
  original interaction
  ```py
  >>> embed : discord.Embed
  ```
  embed to send
  ```py
  >>> failed : bool, (optional)
  ```
  if the request failed (if the request failed, the embed won't be automatically deleted)\\
  defaults to `False`

  ## Returns
  ```py
  Coroutine[Any, Any, None] : the coroutine that sends the embed
  ```
  """
  s: int = 5
  if not failed:
    r = f'\nauto delete {format_timestamp(timestamp=Arrow.utcnow().shift(seconds=s))}'
    try:
      embed.description += r
    except TypeError:
      embed.description = r
  return send_embed(interaction, embed, ephemeral=True, delete_after=s if not failed else None)


def send_status_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
  failed: bool = False,
) -> Coroutine[Any, Any, None]:
  """
  send a status embed\\
  will automatically delete the embed after 5 seconds and add a timestamp to the description

  ## Parameters
  ```py
  >>> interaction : discord.Interaction
  ```
  original interaction
  ```py
  >>> embed : discord.Embed
  ```
  embed to send
  ```py
  >>> failed : bool, (optional)
  ```
  if the request failed (if the request failed, the embed won't be automatically deleted)\\
  defaults to `False`

  ## Returns
  ```py
  Coroutine[Any, Any, None] : the coroutine that sends the embed
  ```
  """
  s: int = 5
  if not failed:
    r = f'\nauto delete {format_timestamp(timestamp=Arrow.utcnow().shift(seconds=s+5))}'
    try:
      embed.description += r
    except TypeError:
      embed.description = r
  channel = interaction.channel
  return channel.send(embed=embed, delete_after=s if not failed else None)


def send_poll_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
  view: discord.ui.View,
) -> Coroutine[Any, Any, None]:
  """
  send a poll embed

  ## Parameters
  ```py
  >>> interaction : discord.Interaction
  ```
  original interaction
  ```py
  >>> embed : discord.Embed
  ```
  embed to send
  ```py
  >>> view : discord.ui.View
  ```
  view to send

  ## Returns
  ```py
  Coroutine[Any, Any, None] : the coroutine that sends the embed
  ```
  """
  return interaction.response.send_message(embed=embed, view=view)


def send_poll_followup_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
) -> Coroutine[Any, Any, None]:
  """
  send a poll followup embed

  ## Parameters
  ```py
  >>> interaction : discord.Interaction
  ```
  original interaction
  ```py
  >>> embed : discord.Embed
  ```
  embed to send

  ## Returns
  ```py
  Coroutine[Any, Any, None] : the coroutine that sends the embed
  ```
  """
  return interaction.followup.send(embed=embed, ephemeral=True)


def send_xp_embed(
  interaction: discord.Interaction,
  embed: discord.Embed,
  view: discord.ui.View,
) -> Coroutine[Any, Any, None]:
  """
  send a poll embed

  ## Parameters
  ```py
  >>> interaction : discord.Interaction
  ```
  original interaction
  ```py
  >>> embed : discord.Embed
  ```
  embed to send
  ```py
  >>> view : discord.ui.View
  ```
  view to send

  ## Returns
  ```py
  Coroutine[Any, Any, None] : the coroutine that sends the embed
  ```
  """
  return interaction.response.send_message(embed=embed, view=view)


def send_channel_message(channel: discord.TextChannel, message: str) -> Coroutine[Any, Any, None]:
  return channel.send(message)


def edit_channel_message(channel: discord.TextChannel, message: str,
                         msg_id: int) -> Coroutine[Any, Any, None]:
  return channel.edit_message(message, msg_id)


def send_channel_file(channel: discord.TextChannel, file: discord.File) -> Coroutine[Any, Any, None]:
  return channel.send(file=file)
