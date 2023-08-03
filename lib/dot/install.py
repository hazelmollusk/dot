import re
from logging import debug, warning, info
from enum import Enum, auto, nonmember
from pathlib import Path
from contextlib import chdir
from .util import command_output
from .rooted import Rooted
from .git import Git

USER_INSTALL = '~/.dot/dot'
SYSTEM_INSTALL = '/usr/share/dot'
GUESSES = [
  USER_INSTALL,
  SYSTEM_INSTALL
]
GIT_ORIGIN = "https://github.com/hazelmollusk/dot"
GIT_PATTERN = '/dot(.git)?$'

class Install(Rooted):
  
  class Mode(Enum):
    UNSET      = auto()
    GIT        = auto()
    NORMAL     = auto()
    DEFAULT    = nonmember(GIT)

  def __init__(self, dot, path=None):
    super().__init__(path)
    self.dot = dot
    self.mode = Install.Mode(Install.Mode.UNSET)

  def detect(self):
    guesses = [ Path(guess).expanduser() for guess in GUESSES ]
    try:
      run_path = Path(__file__).parent
      guesses.insert(0, run_path)
    except:
      warning('could not detect running filename')
    if self.path:
      guesses.insert(0, self.path)
    for guess in guesses:
      if self.guess(guess):
        return True
    self.mode = Install.Mode(Install.Mode.UNSET)
    self.path = None
    return False
  
  def initialize(self, path=None, mode=None):
    if not mode:
      mode = Install.Mode.DEFAULT
    if not path:
      path = self.dot.path / 'dot'
    self.path = path
    if self.guess(self.path):
      info(f'initialize: valid install found at {self.path}')
      return True
    if mode == Install.Mode.GIT:
      if self.path.exists() and not self.path.is_dir():
        raise RuntimeError(f'not a directory: {self.path}')
      if not self.path.exists():
        self.path.mkdir(parents=True)
      with chdir(self.path):
        result = command_output(f'git clone {GIT_ORIGIN} .')
        if not result:
          raise RuntimeError('git clone failed')
    else:
      raise NotImplementedError()

  def is_valid(self):
    return self.detect()

  def guess(self, path):
    # check if we are in a git checkout
    git = Git(path)
    if git.root:
      debug(f'detect: git repo at {git.root}')
      for name, url in git.remotes.items():
        debug(f'detect: remote {name} -> {url}')
        if re.search(GIT_PATTERN, url):
          self.mode = Install.Mode.GIT
          info(f'detect: found at {git.root}')
          self.path = path
          return True
      warning('inside a foreign git repository?')
      return False
    # check if we are in an unpacked directory
    elif (path/'lib'/'dot'/'__init__.py').exists():
      self.mode = Install.Mode.NORMAL
      self.path = path
      return True
    # nothing found
    return False
