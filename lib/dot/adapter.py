import sys
import os
import subprocess
import re
import logging
import curses
from pathlib import Path
from logging import debug, info, warning, error, critical
from argparse import ArgumentParser
from contextlib import chdir, contextmanager
from hashlib import md5

from .rooted import Rooted
from .util import command_output, file_hash
from .configured import Configured


class Adapter(Configured):

    def __init__(self, dot):
        self.dot = dot
        super().__init__(dot.path / 'adapters' / self.name)
        debug(f'adapter {type(self)} - {self.path}')

    @property
    def name(self):
        raise NotImplementedError

    @property
    def links(self):
        raise NotImplementedError

    @property
    def user_dirs(self):
        raise NotImplementedError

    def install(self):
        debug(f'adapter({self.name}): installing')
        self.create_user_dirs()
        for link in self.links:
            self.install_dot_link(link)

    def create_user_dirs(self):
        changed = False
        if self.user_dirs:
            for path in [self.path / p for p in self.user_dirs]:
                if not path.is_dir():
                    path.mkdir(parents=True)
                    changed = True
        return changed

    def install_dot_link(self, link):
        src = self.dot.path / 'adapters' / self.name / link
        dst = self.dot.path.home() / f'.{link}'
        if not src.exists():
            warning(f'install: link {self.name}/{link} not found!')
            return False
        if dst.exists():
            if dst.samefile(src):
                debug(f'install: {self.name}/{link} already installed')
                return True
            debug(f'install: destination link .{link} exists')
            bkup = self.backup_file(dst)
        info(f'install: linking {dst} to {src}')
        dst.symlink_to(src)
