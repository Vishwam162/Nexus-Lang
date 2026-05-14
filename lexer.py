import ply.lex as lex

tokens = (
    'NAME', 'NUMBER', 'STRING', 'LET', 'PRINT', 'IF', 'WHILE', 
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'EQ', 'LT', 'GT', 
    'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN', 'COMMA',
    'INCREASE', 'RANDOM', 'SEMI', 'ASSIGN', 'SERVE', 'BUTTON', 
    'HEADER', 'STYLE', 'ON_CLICK', 'ROUTE', 'VIDEO',
    'FUNC', 'CALL', 'IMPORT', 'SYSTEM', 'MODEL', 'TRAIN', 'PREDICT',
    'AGENT', 'STORE', 'PLAY', 'UPDATE', 'RECT', 'TEXT', 'ON_KEY',
    'PUSH', 'SHIFT', 'AT', 'LEN'
)

reserved = {
    'let': 'LET', 'print': 'PRINT', 'if': 'IF', 'while': 'WHILE',
    'increase': 'INCREASE', 'random': 'RANDOM', 'serve': 'SERVE', 
    'button': 'BUTTON', 'header': 'HEADER', 'style': 'STYLE', 
    'on_click': 'ON_CLICK', 'route': 'ROUTE', 'video': 'VIDEO',
    'func': 'FUNC', 'call': 'CALL', 'import': 'IMPORT', 
    'system': 'SYSTEM', 'model': 'MODEL', 'train': 'TRAIN', 
    'predict': 'PREDICT', 'agent': 'AGENT', 'store': 'STORE',
    'play': 'PLAY', 'update': 'UPDATE', 'rect': 'RECT', 'text': 'TEXT',
    'on_key': 'ON_KEY', 'push': 'PUSH', 'shift': 'SHIFT', 'at': 'AT', 'len': 'LEN'
}

t_PLUS, t_MINUS, t_TIMES, t_DIVIDE, t_MOD = r'\+', r'-', r'\*', r'/', r'%'
t_EQ, t_LT, t_GT = r'==', r'<', r'>'
t_LBRACE, t_RBRACE = r'\{', r'\}'
t_LBRACKET, t_RBRACKET = r'\[', r'\]'
t_LPAREN, t_RPAREN = r'\(', r'\)'
t_COMMA, t_SEMI, t_ASSIGN = r',', r';', r'='

def t_STRING(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME') 
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_COMMENT(t):
    r'//.*'
    pass

def t_error(t):
    print(f"Lexical Error: {t.value[0]} at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
