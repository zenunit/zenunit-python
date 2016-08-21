"""Set Parser
"""
import zuset

tokens = (
    'PYEXPR', 'WHERE', 'VBAR', 'IN', 'ASTERISK', 'COMMA', 'AMPHERSAND',
    'RBRACE', 'LBRACE', 'PLUS','MINUS','DIVIDE', 'AND'
    )

# Tokens

t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
#t_LPAREN  = r'\('
#t_RPAREN  = r'\)'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_VBAR    = r'\|'
t_DIVIDE  = r'/'
t_ASTERISK= r'\*'
t_AMPHERSAND = r'&'
t_COMMA   = r','
#t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
#t_WHITE   = r'[ \t]+'
t_WHERE   = r'where'
t_IN      = r'in'
t_AND      = r'and'
t_PYEXPR  = r'[^\{\}\|,\r\n]+'

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex(debug=0)

# Parsing rules

precedence = (
    ('left','PLUS','MINUS', 'COMMA'),
    ('left','VBAR','DIVIDE', 'AMPHERSAND', 'AND'),
    ('right','ASTERISK', 'WHERE', 'IN'),
    )

def p_compset(t):
    '''compset :  set
        | compset set_op set
    '''

    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 4:
        t[0] = zuset.CompSet()
        t[0].left = t[1]
        t[0].op = t[2]
        t[0].right = t[3]
        zuset.sets.append(t[0])
    else:
        raise Exception('Wrong number of elements: %d'%len(t))


def p_set_op(t):
    '''set_op : VBAR
        | MINUS
        | AMPHERSAND
    '''
        #| PLUS
        #| DIVIDE

    t[0] = t[1]

def p_set(t):
    '''set : LBRACE RBRACE
        | LBRACE elems RBRACE
    '''

    if len(t) == 3:
        t[0] = zuset.Set()
    elif len(t) == 4:
        t[0] = zuset.Set()
        t[0].elems.append(t[2])
    else:
        raise Exception('Wrong number of elements: %d'%len(t))
    zuset.sets.append(t[0])

def p_elems(t):
    '''elems : elem
        | elems COMMA elem
    '''

    elen = len(t) - 1

    if elen == 1:
        t[0] = [t[1]]
    elif elen == 3:
        if t[1] is None:
            t[1] = []
        t[0] = t[1] + [t[3]]
    else:
        raise Exception('Wrong number of elements: %d'%elen)

def p_elem(t):
    '''elem : set
        | PYEXPR
        | set_rule
    '''

    t[0] = t[1]

def p_set_rule(t):
    'set_rule : PYEXPR VBAR PYEXPR opt_where'

    t[0] = zuset.SetRule(zuset.VarTuple(t[1]), zuset.SetCond(t[3]), t[4])

def p_opt_where(t):
    '''opt_where :
        | WHERE wherebodylist
    '''

    if len(t) == 1:
        pass
    elif len(t) == 3:
        t[0] = Where(t[2])
    else:
        raise Exception('Wrong number of elements: %d'%len(t))

def p_wherebodylist(t):
    """wherebodylist : wherebody
        | wherebodylist AND wherebody
    """

    if len(t) == 2:
        t[0] = [t[1]]
    elif len(t) == 4:
        if t[1] is None:
            t[1] = []
        t[0] = t[1] + [t[3]]
    else:
        raise Exception('Wrong number of elements: %d'%len(t))

def p_wherebody(t):
    'wherebody : PYEXPR IN setlike'

    t[0] = WhereBody(zuset.VarTuple(t[1]), t[3])

def p_setlike(t):
    ''' setlike : set
        | PYEXPR
    '''

    t[0] = t[1]

def prep_quote(s):

    strmapid = 0

    if not s: return s
    escape = False
    quotechar = None
    retstr = []
    quotestr = None
    for _s in s:
        if quotestr is None:
            if escape or _s == "\\":
                raise Exception('Wrong escaping')
            elif _s in [ '"', "'" ]:
                quotechar = _s
                quotestr = []
            else:
                retstr.append(_s)
        else:
            if escape:
                quotestr.append(_s)
                escape = False
            elif _s == "\\":
                quotestr.append(_s)
                escape = True
            elif _s in [ '"', "'" ]:
                if quotechar == _s:
                    key = '__ZENUNIT_STRMAP_%d'%strmapid
                    strmapid += 1
                    zuset.strmap[key] = ''.join(quotestr)
                    retstr.append(key)
                    quotestr = None
                else:
                    quotestr.append(_s)
            else:
                quotestr.append(_s)

    return ''.join(retstr)

def prep_paren(s):
    if not s: return s

    parenmapid = 0
    retstr = []
    parenstr = None
    depth = 0
    for _s in s:
        if parenstr is None:
            if _s == '(':
                parenstr = []
                depth += 1
            elif _s == ')':
                raise Exception('Wrong parensis')
            else:
                retstr.append(_s)
        else:
            if _s == '(':
                parenstr.append(_s)
                depth += 1
            elif _s == ')':
                depth -= 1
                if depth == 0:
                    key = '__ZENUNIT_PARENMAP_%d'%parenmapid
                    parenmapid += 1
                    zuset.parenmap[key] = ''.join(parenstr)
                    retstr.append(key)
                    parenstr = None
                else:
                    parenstr.append(_s)
            else:
                parenstr.append(_s)

    return ''.join(retstr)

def preprocess(s):
    s = prep_quote(s)
    s = prep_paren(s)
    return s

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc

def parse(s):
    parser = yacc.yacc(debug=False)
    s = preprocess(s)
    parser.parse(s)
    if len(zuset.sets) == 0:
        raise Exception('No set is defined')
    else:
        return zuset.sets[-1]

if __name__ == "__main__":

    while True:
        try:
            s = raw_input('zenunit > ')   # Use raw_input on Python 2
        except EOFError:
            break
        s = preprocess(s)
        parser = yacc.yacc(debug=True)
        parser.parse(s)
        #import pdb; pdb.set_trace()
        for s in zuset.sets:
            zuset.showtree(s)
        zuset.sets = []
