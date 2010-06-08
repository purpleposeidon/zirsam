# -*- coding: utf-8 -*-

"""
Things common to semantic analysis
"""
from zirsam.common import FastString
import dephora

class Context:
  def __init__(self):
    self.roda = []
    self.provalsi = dephora.ProValsi()

class ParsePass:
  """
  Defines a list of functions that correspond to a node in the parse tree.
  
  """
  def __init__(self, root):
    self.root = root
    self.node = root
  def pull(self, *args):
    return self.node.pull(*args)
  def search(self, *args):
    return self.node.search(*args)
  def __call__(self):
    """Run functions upon nodes"""
    pass
  __orig_functions = set(dir())
    

class Da:
  #Things that are referred to
  def __init__(self, context):
    context.roda.append(self)