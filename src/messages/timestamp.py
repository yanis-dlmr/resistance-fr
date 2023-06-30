from arrow import Arrow

from ..helper import AutoNumberedEnum

__all__ = ['TimestampType', 'format_timestamp']


class TimestampType(AutoNumberedEnum):
  """Timestamp types supported by Discord"""

  SHORT_TIME = (':t')
  LONG_TIME = (':T')

  SHORT_DATE = (':d')
  LONG_DATE = (':D')

  SHORT_DATETIME = ('')
  LONG_DATETIME = (':F')

  RELATIVE = (':R')

  def __init__(self, s: str):
    self.s = s


def format_timestamp(
  timestamp: int | float | Arrow,
  timestamp_type: TimestampType = TimestampType.RELATIVE,
) -> str:
  """
  format a timestamp into a Discord timestamp

  ## Parameters
  ```py
  >>> timestamp : int | float | Arrow
  ```
  timestamp to format (int: unix timestamp, float: unix timestamp in seconds, Arrow: Arrow object)
  ```py
  >>> timestamp_type : TimestampType, (optional)
  ```
  timestamp type to format the timestamp into (see `TimestampType`)\\
  defaults to `TimestampType.RELATIVE`

  ## Returns
  ```py
  str : formatted_timestamp
  ```
  """

  if isinstance(timestamp, int):
    # The timestamp is already an int, leave it as-is
    int_timestamp = timestamp

  elif isinstance(timestamp, float):
    # The timestamp is a float, convert it to an int
    int_timestamp = int(timestamp)

  elif isinstance(timestamp, Arrow):
    # The timestamp is an Arrow object, convert it to an int in UTC
    timestamp = timestamp.to('UTC')
    int_timestamp = timestamp.int_timestamp

  # Combine the timestamp and the format
  return f'<t:{int_timestamp}{timestamp_type.s}>'
