import sys, re
from pathlib import Path
from enum import Enum, auto, nonmember
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
CONFIG_PATH=f'~/.dot'
LOG_LEVEL=WARN
for arg in sys.argv:
  if re.search('--?[a-z]*v', arg):
    LOG_LEVEL=DEBUG


class Dot(Configured, Git):
  
  def __init__(self, params=None, path=None):
    self.params = params
    self.path = path
    self.install = Install(self)

  def setup_logging(self, level=LOG_LEVEL):
    if not level: level = LOG_LEVEL
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
      self.path = self.args.config or CONFIG_PATH
      self.install.detect()
      self.run()
    except Exception as e:
      critical('exception encountered, exiting..')
      if getLogger().level == DEBUG: 
        raise e
      else:
        warning(f'error: {str(e)}')

  @property
  @cache
  def adapters(self):
    self.config.setdefault('adapters', [ a.name for a in Adapter.__subclasses__() ])
    return [ cls(self) for cls in Adapter.__subclasses__() \
            if cls.name in self.config['adapters']]

  def detect_root(self):
    if self.args.root: 
      run_path = Path(self.args.root)
      debug(f'detect: root set -> {run_path}')
    else:
      run_path = Path(__file__).parent
      debug(f'detect: initial run path -> {run_path}')
    git = Git(run_path)
    if git.root:
      debug(f'detect: git repo at {git.root}')
      for name, url in git.remotes.items():
        debug(f'detect: remote {name} -> {url}')
        if re.search(GIT_PATTERN, url):
          self.install_type = Dot.Install.GIT
          info(f'detect: found at {git.root}')
          return git.root
      warning(f'detect: no valid remote found!')
    elif (run_path.parent/'lib'/'dot'/'__init__.py').exists():
      self.install_type = Dot.Install.NORMAL
      return run_path.parent
    else:
      info('no installation detected')
    return None
  
  def run(self):
    debug('running non-interactively')
    if self.args.install:
      self.install(self.path, True)
      for adapter in self.adapters:
        adapter.install()

  # def install(self, path=None, create=False):
  #   if path: self.path = path
  #   if not self.path: self.path = Path.home() / '.dot'
  #   debug(f'install: root -> {self.path}')
  #   if not self.git.root:
  #     if not create:
  #       warning('install: refusing to create new install!')
  #       raise RuntimeWarning('refusing to create new install!')
  #     info(f'install: not detected at {self.path}, cloning from {GIT_ORIGIN}')
  #     self.git.create(GIT_ORIGIN, self.path)
  #   else: 
  #     info(f'install: updating install at {self.path}')
  #     #self.git.update()

  def load_config(self, filename=None, style=None):
    config_path = Path(filename or CONFIG_PATH).expanduser()
    config_vars = {}
    if config_path.exists():
      info(f'config: loading from file {config_path}')
      with open(config_path) as cfg:
        config_vars = dict([ line.split('=', 1) for line in cfg.readlines() ])
        for k, v in config_vars.items(): 
          debug(f'config: {k}={v}')
    return config_vars

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
    parser.add_argument('-c', '--config', type=str,
                        help='root config path')
    parser.add_argument('-m', '--menu', action='store_true',
                        help='show menu interface')
    return parser.parse_args(params)
  
  def run_ui(self):
    DotUI(self).main()
