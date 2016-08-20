
============================
zenunit design documentation
============================




-----
Goals
-----

- Allow user to describe unit testing, rather than to implement
- Generates test cases automatically
- Supports integration testing and beta-user testing


----------
Approaches
----------

- User adds a decorator on the function to be tested.
- User adds set definitions of input and output wihtin docstring.
- zenunit generates test cases based on the set definitions
- zenunit also verifies the set definitions are met during normal program execution too.

--------------------
zenunit set notation
--------------------

::

    set         : {} | { [elems] }  | set set_op set
    set_op      : "|" | "&" ...
    elems       : roster style, rule style..



