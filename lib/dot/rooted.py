from pathlib import Path

class Rooted:

  def __init__(self, path=None):
    if isinstance(path, str):
      path = Path(path)
    if isinstance(path, Path):
      self.path = path
    elif path is not None:
      raise RuntimeError(f'illegal path: {path}')

  @property
  def path(self): return self._path

  @path.setter
  def path(self, path):
    if isinstance(path, str):
      self._path = Path(path)
    elif isinstance(path, Path):
      self._path = path
    elif path is None:
      self._path = None
    else:
      raise RuntimeWarning(f'{type(self)}: cannot assign path to {type(path)}: {path}')
