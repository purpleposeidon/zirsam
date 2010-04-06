

import os

parse_modules = ['orthography', 'morphology', 'thaumatology', 'dendrography']
__all__ = ['config', 'common']+parse_modules+['bnf']
data_path = os.path.join(os.path.split(__file__)[0], 'data')
def resource(name):
  return os.path.join(data_path, name)
