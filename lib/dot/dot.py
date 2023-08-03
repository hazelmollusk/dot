import sys, re
from pathlib import Path
from logging import (
    debug, info, warning, error, critical,
    WARN, DEBUG, getLogger, StreamHandler
)
from argparse import ArgumentParser
from functools import cache
from .rooted import Rooted
from .config import Configured
from .git import Git
from .util import PROGNAME, command_output
from .adapter import Adapter
from .log.color_formatter import ColorFormatter
from .dotui import DotUI  
from .install import Install


#################### default constants ##############
USER_PATH=f'~/.dot'
LOG_LEVEL=WARN
for arg in sys.argv:
  if re.search('--?[a-z]*v', arg):
    LOG_LEVEL=DEBUG
#####################################################


class Dot(Configured, Git):
  
  def __init__(self, path=None, params=None):
    self.params = params
    self.path = path or USER_PATH
    self.install = Install(self)

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
      self.args = self.parse_args()
      self.install.detect()
      self.run()
    except Exception as e:
      critical('exception encountered, exiting..')
      if getLogger().level == DEBUG: 
        raise e
      else:
        error(f'error: {str(e)}')

  @property
  @cache
  def adapters(self):
    config = self.config
    config.setdefault('adapters', [ a.name for a in Adapter.__subclasses__() ])
    debug(str(self.config))
    debug(str(config))
    return [ cls(self) for cls 
                in Adapter.__subclasses__()
                if cls.name in self.config['adapters'] ]
  
  def run(self):
    debug('running non-interactively')
    if self.args.install:
      if not self.install.is_valid():
        self.install.initialize(path=self.path) # TODO: install.mode arg
      for adapter in self.adapters:
        adapter.install()

  def parse_args(self, params=None):
    params = params or self.params or None
    epilog = command_output('ddate') or 'Install `ddate`!'
    parser = ArgumentParser(epilog=epilog)
    parser.add_argument('-i', '--install', action='store_true', 
                        help='install/update')
    parser.add_argument('-r', '--root', type=str, 
                        help='root install path')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='show debugging output')
    parser.add_argument('-m', '--menu', action='store_true',
                        help='show menu interface')
    return parser.parse_args(params)
  
  def run_ui(self):
    DotUI(self).main()
