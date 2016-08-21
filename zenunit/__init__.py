"""
zenunit-python
==============

    Descriptive unit-test generation framework for Python
 
    https://zenunit-python.github.com/

Using
-----

    T.B.D.
"""

#    Copyright (C) 2016 by
#    Youngsung Kim <grnydawn@gmail.com>
#    All rights reserved.
#
# Add platform dependent shared library path to sys.path
#

from __future__ import absolute_import

import sys
if sys.version_info[:2] < (2, 7):
    MSG = "Python 2.7 or later is required for zenunit-python (%d.%d detected)."
    raise ImportError(MSG % sys.version_info[:2])
del sys

# Release data
from zenunit import release

__author__ = '%s <%s>' % release.AUTHORS['Youngsung']
__license__ = release.LICENSE

__date__ = release.DATE
__version__ = release.VERSION

__bibtex__ = """Not published yet."""

# These are import orderwise
from zenunit.exception import zuException, zuError
from zenunit.utils import *

import zenunit.classes
from zenunit.classes import parse
