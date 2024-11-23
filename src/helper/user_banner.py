from discord import User, File

from PIL import Image, ImageFont
import requests
import random
from easy_pil import Editor, load_image


__all__ = ['UserBanner']


class UserBanner():
  """
  Initialize UserBanner class with a list of background image URLs and the server name.

  ## Parameters
  ```py
  >>> background_urls : list[str]
  ```
  List of URLs for background images.
  ```py
  >>> server_name : str, (optional)
  ```
  Server name.
  """
  
  def __init__(self, background_urls: list[str], server_name: str = None):
    self.background_urls = background_urls
    self.server_name = server_name

  def get_banner(self, avatar: User.avatar) -> File:
    """
    Build a banner with the uppercase server name, user profile picture, and background picture.

    ## Parameters
    ```py
    >>> avatar : User.avatar
    ```
    User's avatar.

    ## Returns
    ```py
    >>> file : discord.File
    ```
    Generated banner image file.
    """
    background = Editor(self.get_random_class_picture())
    background.paste(
      image = Editor( load_image(avatar) ).resize((350,350)).circle_image(),
      position = (160, 180)
    )
    background.text(
      position = (660,650),
      text = self.server_name.upper(),
      color = "white",
      font = ImageFont.truetype("assets/fonts/OMEGLE.otf", 50),
      align = "center"
    )
    return File(fp = background.image_bytes, filename = "banane.png")

  def get_random_class_picture(self) -> Image:
    """
    Get a random background image from the provided URLs.

    ## Returns
    ```py
    >>> image : PIL.Image
    ```
    Random background image.
    """
    return Image.open(requests.get(random.choice(self.background_urls), stream=True).raw)
