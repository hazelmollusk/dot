from ..adapter import Adapter

class BashAdapter(Adapter):
  
  @property
  def name(self): return 'bash'
  
  @property
  def links(self): return ['bashrc','bash_profile','bash_aliases']
