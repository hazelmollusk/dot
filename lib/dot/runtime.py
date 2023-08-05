import sys
from functools import cached_property, cache
from argparse import ArgumentParser
from logging import debug, info


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
    debug(('get_parser', obj, parser),)
    p = parser or ArgumentParser()
    o = obj or self.tree
    sps = None
    for name, opts in o.get('_options', {}).items():
      args, kwargs = [], {}
      if short := self.get_short_opt(name):
        args.append(f'-{short}')
      args.append(f'--{name}')
      kwargs.update(opts)
      p.add_argument(*args, **kwargs)
    for sub_name, sub_obj in o.items():
      debug(f'XX {sub_name}')
      if not sub_name.startswith('_'):
        info(f'YY {sub_name}')
        if isinstance(sub_obj, dict):
          if not sps: sps = p.add_subparsers()
          sub_kwargs = sub_obj.get('_command', {})
          # sub_kwargs.setdefault('title', sub_name)
          # sub_kwargs.setdefault('dest', sub_name)
          sub_parser = sps.add_parser(sub_name, **sub_kwargs)
          sub_menu = self.get_parser(sub_obj, sub_parser)

          


    return p

  def parse_args(self, params=None):
    self.params = params or sys.argv[1:]
    return self.get_parser().parse_args(self.params)
