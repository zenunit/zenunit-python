"""Set Parser
"""

tokens = (
    'NAME', 'WHERE', 'VBAR', 'IN', 'ASTERISK', 'COMMA', 'AMPHERSAND',
    'LPAREN','RPAREN','RBRACE', 'LBRACE',
    'PLUS','MINUS','DIVIDE', 'WHITE',
    )

# Tokens

t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_VBAR    = r'\|'
t_DIVIDE  = r'/'
t_ASTERISK= r'\*'
t_AMPHERSAND = r'&'
t_COMMA   = r','
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_WHITE   = r'[ \t]+'
t_WHERE   = r'where'
t_IN      = r'in'

# Ignored characters
#t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex(debug=1)

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','VBAR','DIVIDE', 'AMPHERSAND'),
    ('right','ASTERISK'),
    )

class Set(object):
    def __init__(self):
        self.elems = []

class CompSet(object):
    def __init__(self):
        self.op = None
        self.left = None
        self.right = None

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

# list of sets
sets = []

def p_compset(t):
    '''compset :  set
        | compset opt_WHITE set_op opt_WHITE set
    '''

    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 6:
        t[0] = CompSet()
        t[0].left = t[1]
        t[0].op = t[3]
        t[0].right = t[5]
        sets.append(t[0])
    else:
        raise Exception('Wrong number of elements: %d'%len(t))


def p_set_op(t):
    '''set_op : VBAR
        | PLUS
        | MINUS
        | DIVIDE
        | AMPHERSAND
    '''

    t[0] = t[1]

def p_set(t):
    '''set : LBRACE opt_WHITE RBRACE
        | LBRACE opt_WHITE elems opt_WHITE RBRACE
    '''

    if len(t) == 4:
        t[0] = Set()
        t[0].elems.append(t[2])
    elif len(t) == 6:
        t[0] = Set()
        t[0].elems.append(t[3])
    else:
        raise Exception('Wrong number of elements: %d'%len(t))
    sets.append(t[0])

def p_elems(t):
    '''elems : elem
        | elems opt_WHITE COMMA opt_WHITE elem
    '''

    elen = len(t) - 1

    if elen == 1:
        t[0] = [t[1]]
    elif elen == 5:
        if t[1] is None:
            t[1] = []
        t[0] = t[1] + [t[5]]
    else:
        raise Exception('Wrong number of elements: %d'%elen)

def p_elem(t):
    '''elem : NAME
        | set
    '''

    t[0] = t[1]

#def p_set_blank(t):
#    'set_blank : LBRACE opt_WHITE RBRACE'
#
#    t[0] = Set(t[2])
#
#def p_set_nonblank(t):
#    'set_nonblank : LBRACE opt_WHITE RBRACE'
#
#    t[0] = Set(t[2])

def p_optional_white(t):
    '''opt_WHITE :
        | WHITE'''
    if len(t) > 1:
        t[0] = t[1]
    else:
        t[0] = ''

## dictionary of names
#names = { }
#
#def p_statement_assign(t):
#    'statement : NAME EQUALS expression'
#    names[t[1]] = t[3]
#
#def p_statement_expr(t):
#    'statement : expression'
#    print(t[1])
#
#def p_expression_binop(t):
#    '''expression : expression PLUS expression
#                  | expression MINUS expression
#                  | expression TIMES expression
#                  | expression DIVIDE expression'''
#    if t[2] == '+'  : t[0] = t[1] + t[3]
#    elif t[2] == '-': t[0] = t[1] - t[3]
#    elif t[2] == '*': t[0] = t[1] * t[3]
#    elif t[2] == '/': t[0] = t[1] / t[3]
#
#def p_expression_uminus(t):
#    'expression : MINUS expression %prec UMINUS'
#    t[0] = -t[2]
#
#def p_expression_group(t):
#    'expression : LPAREN expression RPAREN'
#    t[0] = t[2]
#
#def p_expression_number(t):
#    'expression : NUMBER'
#    t[0] = t[1]
#
#def p_expression_name(t):
#    'expression : NAME'
#    try:
#        t[0] = names[t[1]]
#    except LookupError:
#        print("Undefined name '%s'" % t[1])
#        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc(debug=True)

while True:
    try:
        s = raw_input('zenunit > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)
    for s in sets:
        showtree(s)
    sets = []

