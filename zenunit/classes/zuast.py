"""AST related functions

"""

import ast

def hastest(path):
    with open(path, 'r') as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                print(node.name)
            print(node.__class__)
        #import pdb; pdb.set_trace()
    pass



for stmt in ast.walk(self.tree):
    # Ignore non-class
    if not isinstance(stmt, ast.ClassDef):
        continue
    # If it's a class, iterate over its body member to find methods
    for body_item in stmt.body:
        # Not a method, skip
        if not isinstance(body_item, ast.FunctionDef):
            continue
        # Check that it has a decorator
        for decorator in body_item.decorator_list:
            if (isinstance(decorator, ast.Name)
               and decorator.id == 'staticmethod'):
                # It's a static function, it's OK
                break
        else:
            # Function is not static, we do nothing for now
            pass

