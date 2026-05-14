import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'EQ', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS'), 
)

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_statement_simple(p):
    '''statement : CALL NAME SEMI
                 | SYSTEM expression SEMI
                 | PRINT expression SEMI
                 | SERVE expression SEMI
                 | HEADER expression SEMI
                 | VIDEO expression SEMI
                 | IMPORT expression SEMI
                 | MODEL expression SEMI
                 | INCREASE NAME SEMI
                 | SHIFT NAME SEMI
                 | PREDICT expression SEMI'''
    p[0] = (p[1], p[2])

def p_statement_assign(p):
    '''statement : LET NAME ASSIGN expression SEMI
                 | PUSH NAME expression SEMI'''
    if p[1] == 'let': p[0] = ('let', p[2], p[4])
    else: p[0] = ('push', p[2], p[3])

def p_statement_double(p):
    '''statement : STYLE expression expression SEMI
                 | BUTTON expression expression SEMI
                 | TRAIN expression expression SEMI
                 | AGENT expression expression SEMI
                 | STORE expression expression SEMI'''
    p[0] = (p[1], p[2], p[3])

def p_statement_game(p):
    '''statement : PLAY expression expression expression SEMI
                 | RECT expression expression expression expression expression SEMI
                 | TEXT expression expression expression expression SEMI
                 | UPDATE LBRACE statements RBRACE
                 | ON_KEY expression LBRACE statements RBRACE'''
    if p[1] == 'play': p[0] = ('play', p[2], p[3], p[4])
    elif p[1] == 'rect': p[0] = ('rect', p[2], p[3], p[4], p[5], p[6])
    elif p[1] == 'text': p[0] = ('text', p[2], p[3], p[4], p[5])
    elif p[1] == 'update': p[0] = ('update', p[3])
    elif p[1] == 'on_key': p[0] = ('on_key', p[2], p[4])

def p_statement_blocks(p):
    '''statement : FUNC NAME LBRACE statements RBRACE
                 | ROUTE expression LBRACE statements RBRACE
                 | ON_CLICK expression LBRACE statements RBRACE
                 | IF expression LBRACE statements RBRACE
                 | WHILE expression LBRACE statements RBRACE'''
    p[0] = (p[1], p[2], p[4])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | expression EQ expression
                  | expression LT expression
                  | expression GT expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('-', ('num', 0), p[2])

def p_expression_val(p):
    '''expression : NAME
                  | NUMBER
                  | STRING
                  | LPAREN expression RPAREN'''
    if len(p) == 4: p[0] = p[2]
    elif isinstance(p[1], int): p[0] = ('num', p[1])
    elif p.slice[1].type == 'STRING': p[0] = ('str', p[1])
    else: p[0] = ('var', p[1])

def p_error(p):
    if p: print(f"Syntax Error near '{p.value}' at line {p.lineno}")
    else: print("Syntax Error at EOF")

parser = yacc.yacc()
