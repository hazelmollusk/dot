from logging import (
    debug, info, warning, error, critical,
    WARN, DEBUG, getLogger, StreamHandler
)

PROGNAME='dotctl'


################################## inspect #########
from logging import DEBUG, getLogger
from pprint import pformat, isreadable
def inspect(obj, label=None, level=DEBUG, **fmtargs):
  obj_id = f'{type(obj).__name__}(#{id(obj)})'
  output = (label or '') + f'\n\t\x1b[35m▞ ▞ \x1b[36m{obj_id})'
  pfargs = {
  #  'indent': 4,
  #  'depth': None,
  #  'width': 10,
  }
  pfargs.update(fmtargs)
  obj_out = pformat(obj, **pfargs)
  output = f'{output}\n' + '\n'.join([ 
    f'\t\x1b[35m▙▝\t\x1b[36m{line}\x1b[0m'
    for line in obj_out.splitlines() 
  ])
  getLogger().log(level=level, msg=output)


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
def backup_file(filename):
  from pathlib import Path
  file = Path(filename).expanduser()
  bkf = None
  if not file.exists(): 
    warning(f'backup: file {file} not found!')
    return True
  if file.is_dir():
    c = 0
    while (bkf := file.with_suffix(f'.bak.{c}')).exists(): c += 1
  else:  
    bkf = file.with_suffix(f'.bak.{file_hash(file)[0:8]}')
    if bkf.exists():
      warning(f'backup: backup file {bkf} already exists!')
      file.unlink()
      return bkf
  debug(f'backup: {filename} -> {bkf}')
  return file.rename(bkf)


#### format_traceback #####
def format_traceback():
  pass
