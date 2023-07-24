import logging
from typing import Any
from typing_extensions import override
from termcolor import colored

__all__ = ['UsefulFormatter']


def formatter(c: str, attrs: list[str] = None, colored_output: bool = True) -> str:
  if colored_output:
    return f"{colored('%(asctime)s', 'grey', attrs=['bold'])} {colored('%(levelname)8s', c, attrs=attrs)} {colored('%(name)s', 'magenta')} (%(filename)s:%(lineno)d) %(message)s"
  return "%(asctime)s %(levelname)8s %(name)s (%(filename)s:%(lineno)d) %(message)s"


class UsefulFormatter(logging.Formatter):

  dt_fmt = '%Y-%m-%d %H:%M:%S'

  def __init__(self, *args: Any, colored_output: bool = True, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)
    self.colored_output = colored_output

  @override
  def format(self, record: logging.LogRecord) -> str:
    formats = {
      logging.DEBUG: formatter('green', colored_output=self.colored_output),
      logging.INFO: formatter('blue', colored_output=self.colored_output),
      logging.WARNING: formatter('yellow', colored_output=self.colored_output),
      logging.ERROR: formatter('red', colored_output=self.colored_output),
      logging.CRITICAL: formatter('red', ['bold'], colored_output=self.colored_output),
    }
    log_fmt = formats.get(record.levelno)
    fmt = logging.Formatter(log_fmt, self.dt_fmt, style='%')
    return fmt.format(record)
