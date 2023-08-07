import sys
from functools import cached_property, cache
from argparse import ArgumentParser
from logging import WARN, DEBUG, getLogger, StreamHandler
from .util import inspect
from .log.color_formatter import ColorFormatter
from pprint import pprint as pp


class Runtime:

    parser = cached_property(lambda self: self._build_parser)
    params = property(lambda self: self.dot.params or sys.argv[1:])
    global_options = cached_property(
        lambda self: self._build_parser().parse_known_args(self.params)[0])
    used_short_opts = cached_property(lambda self: [])

    def __init__(self, dot):
        self.dot = dot
        self.loaded = False

    def _build_parser(self, obj=None, parent=None, controller=None, title=None):
        parser = ArgumentParser() if parent is None else parent
        controller = self.dot if controller is None else controller
        obj = controller.tree if obj is None else obj
        title = title or 'global'
        subparsers = None
        for name, dfn in obj.items():
            if name == '_options':
                group = parser.add_argument_group(f'{title} options')
                self.parser_add_args(group, dfn)
            elif name.startswith('_'):
                pass
            else:
                subparsers = subparsers or parser.add_subparsers(
                  title=f'{"sub-" if parent is None else ""}commands',
                  help='additional help',
                  description=f'{title} commands'
                )
                parser_kwargs = dfn.get('_config', {})
                title = parser_kwargs.get('title', name)
                subparser = subparsers.add_parser(name, **parser_kwargs)
                self._build_parser(dfn, subparser, title=title)
        return parser

    def cache_clear(self):
        self.parser.cache_clear()
        self.get_short_opt.cache_clear()
        self.used_short_opts.cache_clear()
        self.tree.cache_clear()

    def initialize(self):
        self.cache_clear()
        self.loaded = True
        return self.loaded

    @cache
    def get_short_opt(self, name):
        for c in name:
            if c not in self.used_short_opts:
                self.used_short_opts.append(c)
                return c
        return False

    def parser_add_args(self, parser, arg_defs):
        for name, options in arg_defs.items():
            short = self.get_short_opt(name)
            args = filter(None, [
                f'-{short}' if short else None,
                f'--{name}'])
            kwargs = {}
            if options['type'] == bool:
                kwargs['action'] = 'store_true' \
                    if not options.get('default', False) \
                    else 'store_false'
            elif options['type'] in (str, int):
                kwargs['type'] = options['type']
            for opt in ('required', 'help', 'metavar',
                        'default', 'nargs', 'action'):
                if opt in options:
                    kwargs[opt] = options[opt]
            parser.add_argument(*args, **kwargs)

    # def get_parser(self, obj=None, parser=None):
    #     p = parser or self.parser
    #     o = obj or self.tree
    #     inspect(o, 'get_parser(<OBJ>, parser)')

    #     ############# add --options ###########
    #     options = o.get('_options', {})
    #     for opt_name, opt_params in options.items():
    #         debug({'opt_name': opt_name, 'opt_params': opt_params})
    #         args, kwargs = [], {}
    #         if short := self.get_short_opt(opt_name):
    #             args.append(f'-{short}')
    #         args.append(f'--{opt_name}')
    #         kwargs.update(opt_params)
    #         debug({
    #             'p': p,
    #             'args': args,
    #             'kwargs': kwargs
    #         })
    #         p.add_argument(*args, **kwargs)

    #     ############# add subcommands ############
    #     sps = None
    #     for sub_name, sub_obj in o.items():
    #         if not sub_name.startswith('_'):
    #             if isinstance(sub_obj, dict):
    #                 info(
    #                     f'--- I think we are descending into {sub_name} - {sub_obj}')
    #                 if not sps:
    #                     sps = p.add_subparsers()
    #                 sub_kwargs = sub_obj.get('_command', {})
    #                 sub_parser = sps.add_parser(sub_name, **sub_kwargs)
    #                 sub_menu = self.get_parser(sub_obj, sub_parser)
    #     return p

    def options(self):
        return self.parser.parse_args(self.params) if self.initialize() else {}
