import sys, re
from pathlib import Path
from logging import (
    debug, info, warning, error, critical,
    WARN, DEBUG, getLogger, StreamHandler
)
from argparse import ArgumentParser
from functools import cache, cached_property
from .rooted import Rooted
from .configured import Configured
from .git import Git
from .util import PROGNAME, command_output
from .adapter import Adapter
from .log.color_formatter import ColorFormatter
from .dotui import DotUI  
from .install import Install
from .runtime import Runtime


#################### default constants ##############
USER_PATH=f'~/.dot'
LOG_LEVEL=WARN
for arg in sys.argv:
  if re.search('--?[a-z]*v', arg):
    LOG_LEVEL=DEBUG
#####################################################


class Dot(Configured, Git):

  # @property
  # def run(self): return Runtime(self)
  # @property
  # def install(self): return Install(self)
  run = property(lambda self: Runtime(self))
  install = property(lambda self: Install(self))
    
  def __init__(self, path=None, params=None):
    self.params = params
    self.path = path or Path(USER_PATH).expanduser()

  def setup_logging(self, level=LOG_LEVEL):
    logger = getLogger()
    logger.setLevel(level)
    ch = StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(ColorFormatter())
    logger.addHandler(ch)

  def main(self):
    self.setup_logging(LOG_LEVEL)
    try:
      self.args = self.run.parse_args()
      self.install.detect()
    except Exception as e:
      critical(f'error: {str(e)}')
      if getLogger().level == DEBUG: 
        raise e

  @cached_property
  def adapters(self):
    config = self.config
    config.setdefault('adapters', [ a.name for a in Adapter.__subclasses__() ])
    return [  cls(self) for cls 
              in Adapter.__subclasses__()
              if cls.name in self.config['adapters'] ]
  
  def runit(self):
    debug('running non-interactively')
    if self.args.install:
      
      if not self.install.is_valid():
        self.install.initialize(path=self.path) # TODO: install.mode arg
      for adapter in self.adapters:
        adapter.install()
