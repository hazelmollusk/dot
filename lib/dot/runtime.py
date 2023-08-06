import sys
from functools import cached_property, cache
from argparse import ArgumentParser
from logging import debug, info, warn, error
from .util import inspect

class Runtime:

  def __init__(self, dot):
    self.dot = dot

  def clear_cache(self):
    self.get_short_opt.cache_clear()
    self.used_opts.cache_clear()
    self.tree.cache_clear()

  def get_short_opt(self, name):
    for c in name:
      if c not in self.used_opts:
        self.used_opts.append(c)
        return c
    return False

  @property
  def used_opts(self):
    return []

  @property
  def tree(self):
    t = {
      'setup': {
        '_command': {
          'help': 'set things up'
        },
        '_options': {
          'method': {
            'type': str
          }
        }
      },
      'test': {
        'system': {
          '_options':{
            'type': bool,

          }
        }
      },
      '_options': {
        'verbose': {
          'type': bool,
          'default': False
        }
      }
    }
    return t

  def get_parser(self, obj=None, parser=None):
    warn(('!!!!!!!!!!!','get_parser', obj, parser),)
    p = parser or ArgumentParser()
    o = obj or self.tree
    inspect(o)

    ############# add --options ###########
    options = o.get('_options', {})
    for opt_name, opt_params in options.items():
      debug({'opt_name': opt_name, 'opt_params': opt_params})
      args, kwargs = [], {}
      if short := self.get_short_opt(opt_name):
        args.append(f'-{short}')
      args.append(f'--{opt_name}')
      kwargs.update(opt_params)
      debug({
        'p':p,
        'args':args,
        'kwargs':kwargs
      })
      p.add_argument(*args, **kwargs)

    ############# add subcommands ############
    sps = None
    for sub_name, sub_obj in o.items():
      if not sub_name.startswith('_'):
        if isinstance(sub_obj, dict):
          info(f'--- I think we are descending into {sub_name} - {sub_obj}')
          if not sps: sps = p.add_subparsers()
          sub_kwargs = sub_obj.get('_command', {})
          sub_parser = sps.add_parser(sub_name, **sub_kwargs)
          sub_menu = self.get_parser(sub_obj, sub_parser)
    return p

  def parse_args(self, params=None):
    self.params = params or sys.argv[1:]
    return self.get_parser().parse_args(self.params)
