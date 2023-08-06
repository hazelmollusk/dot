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

from .util import curses_screen, PROGNAME


class DotUI:
    def __init__(self, dot):
        self.dot = dot
        self.main_window = None
        self.windows = []

    def push_window(self, h, w):
        parent = self.windows[len(self.windows) - 1] \
            if self.windows else self.main_window
        lines, cols = parent.getmaxyx()
        w = min(lines - 2, w)
        h = min(cols - 2, h)
        z = self.layer * 3
        window = parent.subwin(h, w, z, z)
        self.windows.append(window)
        return window

    @property
    def layer(self):
        return len(self.windows)

    def menu(self, options, title=None):
        width = max(len(title or '') - 2, *
                    [len(label)+4 for label, func in options])
        height = 5 + len(options)
        # window = parent.subwin(height, width, self.layer * 3, self.layer * 3)
        window = self.push_window(height, width)
        window.border()
        if title:
            self.window_title(window, title)
        options_dict = dict(enumerate(options))
        for idx, (label, func) in options_dict.items():
            window.addstr(idx + 1, 3, f'{idx}. {label}')
        window.refresh()
        while True:
            key = window.getkey()

    def main(self):
        with curses_screen() as screen:
            screen.clear()
            self.main_window = curses.newwin(curses.LINES, curses.COLS)
            self.window_title(self.main_window, PROGNAME)
            self.menu((
                ('Install', lambda: self.dot.install()),
                ('Configure', lambda: self.configure()),
                ('Quit', lambda: self.quit()),
            ), PROGNAME)

    def quit(code=0):
        debug('byee..')
        sys.exit(code)

    def window_title(self, window, text):
        sy, sx = window.getparyx()
        if sy < 0:
            sy = 0
        if sx < 0:
            sx = 0
        lines, cols = window.getmaxyx()
        x = min(sx+2, int(cols/2 - len(text)/2) - sx)
        debug(f'window.addstr({sy}, {x}, {text[0:lines-sx-1]})')
        # raise RuntimeError((f'window.addstr({sy}, {x}, {text[0:lines-sx-1]})'))
        window.addstr(sy, sx+2, text[0:cols-sx-3])


if __name__ == '__main__':
    Dot().main()
