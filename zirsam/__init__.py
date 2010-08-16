# -*- coding: utf-8 -*-


"""
zirsam, by purpleposeidon
"""

import os

PARSE_MODULES = ['orthography', 'morphology', 'thaumatology', 'dendrography']
__all__ = ['config', 'common']+PARSE_MODULES+['bnf']
DATA_PATH = os.path.join(os.path.split(__file__)[0], 'data')
def resource(name):
    """Get the name of a file"""
    return os.path.join(DATA_PATH, name)
