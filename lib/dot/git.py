
import sys, os, subprocess, re, logging, curses
from pathlib import Path
from logging import debug, info, warning, error, critical
from argparse import ArgumentParser
from contextlib import chdir, contextmanager
from hashlib import md5

from .rooted import Rooted
from .util import command_output

class Git(Rooted):

  @property
  def root(self):
    if self.path:
      p = self.path
      while p.parents:
        if (p / '.git' / 'config').exists():
          return p
        p = p.parent
    return None

  @property
  def remotes(self):
    ret = {}
    if self.root:
      with chdir(self.root):
        for line in command_output('git remote -v').splitlines():
          name, url = line.split()[0:2]
          ret[name] = url
    return ret

  def create(self, url=None, path=None):
    if path: self.path = path
    if not self.path:
      error('cannot create without path')
      raise RuntimeError
    debug(f'creating dir {self.path}')
    os.makedirs(self.path, exist_ok=True)
    with chdir(self.path):
      if not command_output(f'git {f"clone {url} {self.path}" if url else "init"}'):
        raise RuntimeError

  def update(self):
    if not self.root:
      raise RuntimeError('cannot update invalid repository!')
    with chdir(self.path):
      if not command_output(f'git pull --all'):
        raise RuntimeError
