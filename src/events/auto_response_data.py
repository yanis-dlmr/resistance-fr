from dataclasses import dataclass

__all__ = ['AutoResponseData']


@dataclass
class AutoResponseData:
  triggers: list[str]
  emotes: list[str] = []
  answer: str = ''
  reply: bool = False

  def __post_init__(self):
    pass

  @classmethod
  def from_json(cls, json: dict[str, list[str] | str | bool]) -> 'AutoResponseData':
    return cls(**json)
