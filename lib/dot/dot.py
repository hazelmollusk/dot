import sys, os, subprocess, re, logging, curses
from pathlib import Path
from logging import debug, info, warning, error, critical
from argparse import ArgumentParser
from contextlib import chdir, contextmanager
from hashlib import md5
from .rooted import Rooted
from .git import Git
from .util import ColorFormatter, PROGNAME, command_output
from .adapter import Adapter

######################## default constants ##############
INSTALL_METHOD="git"
GIT_ORIGIN="https://github.com/hazelmollusk/dot"
# GIT_PATTERN="\/dot(\.git)?\$"
GIT_PATTERN='\\/dot\\.git\\$'
LOG_LEVEL=logging.WARN
for arg in sys.argv:
  if re.search('--?[a-z]*v', arg):
    LOG_LEVEL=logging.DEBUG
CONFIG_PATH=f'~/.dot.json'
# UI_ARG_COUNT = 1
from .log import ColorFormatter



class Dot(Rooted):
    
  def __init__(self, params=None, path=None):
    self.params = params
    self.path = path

  def setup_logging(self, level=LOG_LEVEL):
    if not level: level = LOG_LEVEL
    logger = logging.getLogger()
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(ColorFormatter())
    logger.addHandler(ch)

  def main(self):
    self.setup_logging(LOG_LEVEL)
    try:
      self.args = self.parse_args()
      self.config = self.load_config(self.args.config or CONFIG_PATH)
      self.path = self.detect_root()
      self.run() if ((len(sys.argv) < (3 if self.args.verbose else 2)) \
                     and not self.args.menu) else self.run_ui() 
    except Exception as e:
      critical('exception encountered, exiting..')
      if logging.getLogger().level == logging.DEBUG: 
        raise e
      else:
        warning(f'error: {str(e)}')

  @property
  def git(self):
    return Git(self.path)

  @property
  def home(self):
    return Path.home()

  @property
  def adapters(self):
    self.config.setdefault('adapters', [ a.name for a in Adapter.__subclasses__() ])
    if isinstance(self.config['adapters'], str):
      self.config['adapters'] = self.config['adapters'].split()
    # TODO: memoize?
    return [ cls(self) for cls in Adapter.__subclasses__() \
            if cls.name in self.config['adapters']]

  def detect_root(self):
    if self.args.root: 
      self.path = self.args.root
      return self.path
    run_path = Path('.')
    try: run_path = Path(__file__).parent
    except NameError: pass
    debug(f'detect: initial run path -> {run_path}')
    debug(f'detect: real run path -> {run_path.absolute()}')
    git = Git(run_path)
    if git.root:
      for name, url in git.remotes.items():
        debug(f'detect: remote {name} -> {url}')
        if re.search(GIT_PATTERN, url):
          info(f'detect: found at {git.root}')
          return git.root
    elif (run_path.parent / 'bin' / 'dotctl').exists():
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

  def install(self, path=None, create=False):
    if INSTALL_METHOD=='git':
      if path: self.path = path
      if not self.path: self.path = Path.home() / '.dot'
      debug(f'install: root -> {self.path}')
      if not self.git.root:
        if not create:
          warning('install: refusing to create new install!')
          raise RuntimeWarning('refusing to create new install!')
        info(f'install: not detected at {self.path}, cloning from {GIT_ORIGIN}')
        self.git.create(GIT_ORIGIN, self.path)
      else: 
        info(f'install: updating install at {self.path}')
        self.git.update()
    else:
      warning('install: invalid INSTALL_METHOD!')
      raise RuntimeWarning('invalid install method!')

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
                        help='config file location')
    parser.add_argument('-m', '--menu', action='store_true',
                        help='show menu interface')
    return parser.parse_args(params)
  
  def run_ui(self):
    curses.wrapper(DotUI(self).main())
