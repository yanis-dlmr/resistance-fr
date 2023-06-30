from enum import Enum

__all__ = ['AutoNumberedEnum']


class AutoNumberedEnum(Enum):
  """
  An enum that automatically assigns values to its members.\\
  Just inherit from this class instead of `Enum` and you're good to go.

  ## Example
  ```py
  >>> class MyEnum(AutoNumberedEnum):
  ...   FOO = ()
  ...   BAR = ()
  ...   BAZ = ()
  ...
  >>> MyEnum.FOO
  <MyEnum.FOO: 1>
  >>> MyEnum.BAR
  <MyEnum.BAR: 2>
  >>> MyEnum.BAZ
  <MyEnum.BAZ: 3>
  ```
  """

  def __new__(cls, *args) -> 'AutoNumberedEnum':
    """
    Creates a new enum member.

    ## Returns
    ```py
    object : AutoNumberedEnum
    ```
    """
    value = len(cls.__members__) + 1
    obj = object.__new__(cls)
    obj._value_ = value
    return obj

  def __repr__(self) -> str:
    """
    Returns the representation of this enum member.

    ## Returns
    ```py
    str : str
    ```
    """
    return f'<{self.__class__.__name__}.{self.name}: {self.value}>'

  def __str__(self) -> str:
    """
    Returns the string representation of this enum member.

    ## Returns
    ```py
    str : str
    ```
    """
    return f'{self.__class__.__name__}.{self.name}'

  def __ge__(self, other: 'AutoNumberedEnum') -> bool:
    if self.__class__ is other.__class__:
      return self.value >= other.value
    return NotImplemented

  def __gt__(self, other: 'AutoNumberedEnum') -> bool:
    if self.__class__ is other.__class__:
      return self.value > other.value
    return NotImplemented

  def __le__(self, other: 'AutoNumberedEnum') -> bool:
    if self.__class__ is other.__class__:
      return self.value <= other.value
    return NotImplemented

  def __lt__(self, other: 'AutoNumberedEnum') -> bool:
    if self.__class__ is other.__class__:
      return self.value < other.value
    return NotImplemented
