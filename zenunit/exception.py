# -*- coding: utf-8 -*-
"""
**********
Exceptions
**********

Base exceptions and errors for zenunit.

"""
__author__ = """Youngsung Kim (grnydawn@gmail.com)"""
#    Copyright (C) 2016 by
#    Youngsung Kim <grnydawn@gmail.com>
#    All rights reserved.
#

# Exception handling

# the root of all Exceptions
class zuException(Exception):
    """Base class for exceptions in zenunit."""

class zuError(zuException):
    """Exception for a serious error in zenunit"""
