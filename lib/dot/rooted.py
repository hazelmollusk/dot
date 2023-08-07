from pathlib import Path


class Rooted:

    def __init__(self, path=None):
        if isinstance(path, str):
            path = Path(path)
        if isinstance(path, Path):
            self.path = path
        elif path is not None:
            raise RuntimeError(f'illegal path: {path}')
        else:
            self.path = None

    @property
    def path(self): return self._path

    @path.setter
    def path(self, path):
        if isinstance(path, str):
            self._path = Path(path).expanduser()
        elif isinstance(path, Path):
            self._path = path
        elif path is None:
            self._path = None
        else:
            err = f'{type(self)}: invalid path {path}'
            raise RuntimeWarning(err)
