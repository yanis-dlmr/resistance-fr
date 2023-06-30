import logging
from typing_extensions import override
from termcolor import colored

__all__ = ['UsefulFormatter']


def formatter(c: str, attrs: list[str] = []) -> str:
  return f"{colored('%(asctime)s', 'grey', attrs=['bold'])} {colored('%(levelname)8s', c, attrs=attrs)} {colored('%(name)s', 'magenta')} (%(filename)s:%(lineno)d) %(message)s"


class UsefulFormatter(logging.Formatter):

  dt_fmt = '%Y-%m-%d %H:%M:%S'
  FORMATS = {
    logging.DEBUG: formatter('green'),
    logging.INFO: formatter('blue'),
    logging.WARNING: formatter('yellow'),
    logging.ERROR: formatter('red'),
    logging.CRITICAL: formatter('red', ['bold']),
  }

  @override
  def format(self, record: logging.LogRecord) -> str:
    log_fmt = self.FORMATS.get(record.levelno)
    formatter = logging.Formatter(log_fmt, self.dt_fmt, style='%')
    return formatter.format(record)
