from logging import debug, info, warning, error, critical

PROGNAME='dotctl'


# executes `command` and returns output on success, or False on error
from subprocess import run, PIPE, DEVNULL
def command_output(command):
  info(f'command line: {str(command)}')
  if type(command) == str: 
    command = command.split()
  result = run(command, stdout=PIPE, stderr=DEVNULL)
  result_debug = '\n'.join([ f'\t{line}' for line in result.stdout.decode().strip().splitlines() ])
  debug(f'output: \n\x1b[33m{result_debug}\x1b[0m')
  return result.returncode or result.stdout.decode()


# TODO integrate curses.wrapper()?
##### context wrapper for curses terminal settings ##
from contextlib import chdir, contextmanager
@contextmanager
def curses_screen():
  import curses
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


################### md5 file_hash ############### 
def file_hash(file):
  from hashlib import md5
  return md5(open(file, 'rb').read()).hexdigest()


########################### backup_file #####################
def backup_file(self, filename):
  from pathlib import Path
  file = Path(filename).expanduser()
  if not file.exists(): 
    warning(f'backup: file {file} not found!')
    return True
  h = file_hash(file)
  bkf = Path(f'{filename}.bak.{h[0:8]}')
  if bkf.exists():
    warning(f'backup: backup file {bkf} already exists!')
    file.unlink()
    return bkf
  debug(f'backup: {filename} -> {bkf}')
  return file.rename(bkf)
