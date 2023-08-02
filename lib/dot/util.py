from logging import debug, info, warning, error, critical
from .log import ColorFormatter

PROGNAME='dotctl'

# executes `command` and returns output on success, or False on error
from subprocess import run, PIPE, DEVNULL
def command_output(command):
  debug(f'run: {str(command)}')
  if type(command) == str: 
    command = command.split()
  result = run(command, stdout=PIPE, stderr=DEVNULL)
  debug(f'run: {result.stdout.decode()}')
  return False if result.returncode else result.stdout.decode()


##### context wrapper for curses terminal settings ##
import curses
from contextlib import chdir, contextmanager
@contextmanager
def curses_screen():
    try:
      screen = curses.initscr()
      curses.curs_set(False)  #| no cursor            |#  
      curses.noecho()         #| silence keystrokes   |#
      curses.cbreak()         #| unbuffered input     |#
      screen.keypad(True)     #| handle special keys  |#
      yield screen
    finally:
      curses.curs_set(True) 
      curses.nocbreak()
      screen.keypad(False)
      curses.echo()
      curses.endwin()


########## helpful for debugging curses #######
def ouch(*args, **kwargs):
  raise RuntimeError(*[repr(arg) for arg in args], repr(kwargs))


################### file_hash ############### 
def file_hash(file):
  from hashlib import md5
  return md5(open(file, 'rb').read()).hexdigest()
