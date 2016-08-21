"""Set classes

"""

# globals
sets = []
strmap = {}
parenmap = {}

class SetBase(object):
    """Base class for Set-like classes

    Overview
    --------

        This class provides interface to check if an object is an element of this set
        and to generate a subset of this set
    """

    def exists(self, obj):
        raise Exception('Subclass should implement this method.')

    def subset(self, obj):
        raise Exception('Subclass should implement this method.')

class Set(SetBase):
    def __init__(self):
        self.elems = []

class CompSet(SetBase):
    def __init__(self):
        self.op = None
        self.left = None
        self.right = None

class SetRule(object):
    def __init__(self, vartuple, setcond, where):
        pass

class VarTuple(object):
    def __init__(self, expr):
        pass

class SetCond(object):
    def __init__(self, expr):
        pass

class Where(object):
    def __init__(self, vartuple, setexpr):
        pass

def showtree(obj, depth=0):
    TAB = 4
    if isinstance(obj, Set):
        print ' '*TAB*depth + 'SET'
        for elem in obj.elems:
            if isinstance(obj, Set):
                showtree(elem, depth=depth+1)
            else:
                print ' '*TAB*depth + 'ELEM: %s'%str(elem)
    elif isinstance(obj, CompSet):
        print ' '*TAB*depth + 'COMPSET' +str([obj.op, obj.left, obj.right])
    else:
        print ' '*TAB*depth + 'ELEM: %s'%str(obj)
