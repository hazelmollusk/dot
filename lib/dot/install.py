import re
from logging import debug, warning, info
from enum import Enum, auto, nonmember
from pathlib import Path
from .rooted import Rooted
from .git import Git


GUESSES = [
  '/usr/share/dot',
  '~/.dot/dot'
]
GIT_ORIGIN="https://github.com/hazelmollusk/dot"
GIT_PATTERN='/dot(.git)?$'

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
    guesses = [ Path(guess) for guess in GUESSES ]
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
    # check if we are in an unpacked directory
    elif (path/'lib'/'dot'/'__init__.py').exists():
      self.mode = Install.Mode.NORMAL
      self.path = path
      return True
    # nothing found
    return False
