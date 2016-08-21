"""Simple math functions for testing zenunit

"""

import zenunit as zu

@zu.runtest()
def addtwo(a, b):
    """Adding two numbers

    Parameter
    ---------

        a : :zenunit:`{ x | True where x in NUMBER}`
        b : :zenunit:`{ x | True where x in NUMBER}`

    Returns
    -------

        :zenunit:`{ x | x == a + b where x in NUMBER}`
    """

    return a + b
