import ply.lex as lex

# =========================================================
# ЛЕКСЕР
# =========================================================

tokens = (
    'ASSIGN',

    'EQ',
    'NEQ',
    'LT',
    'GT',

    'MINUS',
    'POWER',

    'QUESTION',

    'LPAREN',
    'RPAREN',

    'LBRACKET',
    'RBRACKET',

    'SEMICOLON',

    'NUMBER',
    'IDENTIFIER',
)

# ---------------------------------------------------------
# Операторы и разделители
# ---------------------------------------------------------

t_ASSIGN = r':='

t_EQ = r'=='
t_NEQ = r'!='
t_LT = r'<'
t_GT = r'>'

t_MINUS = r'-'
t_POWER = r'\^'

t_QUESTION = r'\?'

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_SEMICOLON = r';'

# ---------------------------------------------------------
# Константы
# ---------------------------------------------------------

MAX_IDENT_LEN = 10

# ---------------------------------------------------------
# Восьмеричные числа
# ---------------------------------------------------------

def t_NUMBER(t):
    r'0[0-7]*'
    t.value = int(t.value, 8)
    return t

# ---------------------------------------------------------
# Идентификаторы
# Фиксированная длина
# Внутри могут быть пробелы
# ---------------------------------------------------------

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'

    # удаляем внутренние пробелы
    name = ''.join(t.value.split())

    # фиксированная длина
    if len(name) < MAX_IDENT_LEN:
        name = name.ljust(MAX_IDENT_LEN)

    if len(name) > MAX_IDENT_LEN:
        name = name[:MAX_IDENT_LEN]

    t.value = name

    return t

# ---------------------------------------------------------

t_ignore = ' \t'

# ---------------------------------------------------------

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ---------------------------------------------------------

def t_error(t):
    print(f"Недопустимый символ '{t.value[0]}'")
    t.lexer.skip(1)

# ---------------------------------------------------------

lexer = lex.lex()

# =========================================================
# AST
# =========================================================

class IfNode:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class AssignNode:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

class BinOpNode:
    def __init__(self, op, left, right=None):
        self.op = op
        self.left = left
        self.right = right

class NumberNode:
    def __init__(self, value):
        self.value = value

class VariableNode:
    def __init__(self, name, index=None):
        self.name = name
        self.index = index

# =========================================================
# ПРИОРИТЕТЫ
# =========================================================

precedence = (
    ('left', 'MINUS'),
    ('left', 'POWER'),
)