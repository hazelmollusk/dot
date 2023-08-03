from functools import cache
from .rooted import Rooted
from json import loads

CONFIG_FILENAME = 'config.json'


class Configured(Rooted):

  @property
  def config(self):
    if self.path:
      path = self.path / CONFIG_FILENAME
      if path.exists():
        return self.load_config(path)
    return {}

  @cache
  def load_config(self, path):
    return loads(path.read_text())
