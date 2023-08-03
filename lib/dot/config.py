from functools import cache
from json import loads, dump
from logging import warning
from .rooted import Rooted

CONFIG_FILENAME = 'config.json'


class Configured(Rooted):

  @property
  def config(self):
    if self.path:
      path = self.path / CONFIG_FILENAME
      return self.load_config(path)
    warning('config: path not set!')
    return None

  @cache
  def load_config(self, path):
    return loads(path.read_text()) if path.exists() else {}

  def write_config(self):
    if not self.path:
      raise RuntimeError()
    if not self.path.is_dir():
      if self.path.exists():
        raise RuntimeError(f'config: {self.path} is not a directory!')
    path = self.path / CONFIG_FILENAME
    with path.open('w') as fp :
      dump(self.config, fp)
