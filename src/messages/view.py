from typing import Optional, Callable
from typing_extensions import override

import discord

__all__ = ['CustomView']


class CustomView(discord.ui.View):

  def __init__(self, orig_inter: discord.Interaction, timeout: Optional[int] = None):
    super().__init__()
    self.interaction = orig_inter
    self.timeout = timeout

  async def disable_all_items(self) -> None:
    """
    disable all items in the view
    """
    for item in self.children:
      item.disabled = True
    await self.update()

  @override
  async def on_timeout(self) -> None:
    await self.disable_all_items()

  def __with_item(self, item: discord.ui.Item) -> 'CustomView':
    return self.add_item(item)

  async def update(self) -> None:
    """ update the view """
    try:
      await self.interaction.edit_original_response(view=self)
    except discord.NotFound:
      pass

  def with_button(
    self,
    emoji: str | discord.Emoji | discord.PartialEmoji,
    label: str = None,
    custom_id: str = None,
  ) -> 'CustomView':
    return self.__with_item(discord.ui.Button(emoji=emoji, label=label, custom_id=custom_id))

  def with_button_callback(
    self,
    emoji: str | discord.Emoji | discord.PartialEmoji,
    label: str = None,
    custom_id: str = None,
    callback: Callable[[discord.Interaction], None] = None,
  ) -> 'CustomView':
    button = discord.ui.Button(emoji=emoji, label=label, custom_id=custom_id)
    button.callback = callback
    return self.__with_item(button)

  def with_select(
    self,
    options: list[discord.SelectOption],
    placeholder: str = None,
    custom_id: str = None,
  ) -> 'CustomView':
    return self.__with_item(discord.ui.Select(options=options, placeholder=placeholder, custom_id=custom_id))

  def edit_button(self, custom_id: str, **kwargs) -> 'CustomView':
    for item in self.children:
      if isinstance(item, discord.ui.Button) and item.custom_id == custom_id:
        for key, value in kwargs.items():
          setattr(item, key, value)
        break
    return self
