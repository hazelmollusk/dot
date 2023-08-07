import sys
import re
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
from .util import command_output
from .adapter import Adapter
from .log.color_formatter import ColorFormatter
# from .dotui import DotUI
from .install import Install
from .runtime import Runtime
from .tree import Tree


class Dot(Configured, Git, Tree):

    run = cached_property(lambda self: Runtime(self))
    install = cached_property(lambda self: Install(self))

    def __init__(self, path=None, params=None):
        self.params = params
        self.path = path

    def main(self):
        self.process_global_options()
        try:
            self.install.detect()
        except Exception as e:
            critical(f'error: {str(e)}')
            if getLogger().level == DEBUG:
                raise e

    @property
    def tree(self):
        return {
            'setup': {
                '_options': {
                    'force': {
                        'type': bool,
                        'help': 'use the crowbar'}},
                '_config': {
                    'help': 'configure installation'}},
            '_options': {
                'verbose': {
                    'type': bool,
                    'help': 'enable debug logging'},
                'config': {
                    'type': str,
                    'help': 'user config path',
                    'default': '~/.dot'},
                'root': {
                    'type': str,
                    'help': 'root installation path'}},
        }

    @cached_property
    def adapters(self):
        config = self.config
        config.setdefault(
            'adapters', [a.name for a in Adapter.__subclasses__()])
        return [cls(self) for cls
                in Adapter.__subclasses__()
                if cls.name in self.config['adapters']]

    def setup_logging(self, level=WARN):
        logger = getLogger()
        logger.setLevel(level)
        ch = StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(ColorFormatter())
        logger.addHandler(ch)

    def process_global_options(self):
        opts = self.run.global_options
        level = DEBUG if opts.verbose else WARN
        self.setup_logging(level)
        if opts.config:
            self.path = opts.config
        if opts.root:
            self.install.path = opts.root

    def runit(self):
        debug('running non-interactively')
        if self.args.install:

            if not self.install.is_valid():
                # TODO: install.mode arg
                self.install.initialize(path=self.path)
            for adapter in self.adapters:
                adapter.install()
