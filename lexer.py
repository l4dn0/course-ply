import ply.lex as lex

tokens = (
    'IF', 'ADD', 'SUB', 'MUL', 'DIV', 'CONCAT', 'SUBSTR',
    'EQ', 'NEQ', 'AND', 'GT', 'LT', 'GTE', 'LTE',
    'NUMBER', 'IDENTIFIER', 'FIELD',
    'ASSIGN', 'LPAREN', 'RPAREN', 'DOT', 'SEMICOLON', 'LBRACE', 'RBRACE'
)

t_ASSIGN    = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_DOT       = r'\.'
t_SEMICOLON = r';'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'

def t_KEYWORDS(t):
    r'if|add|sub|mul|div|concat|substr|eq|neq|and|gt|lt|gte|lte'
    keywords = {
        'if': 'IF', 
        'add': 'ADD', 'sub': 'SUB', 'mul': 'MUL', 'div': 'DIV',
        'concat': 'CONCAT', 'substr': 'SUBSTR',
        'eq': 'EQ', 'neq': 'NEQ', 'and': 'AND',
        'gt': 'GT', 'lt': 'LT', 'gte': 'GTE', 'lte': 'LTE',
    }
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t

MAX_IDENT_LEN = 10

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*[ ]*'  # значимые символы, затем пробелы
    t.value = t.value.rstrip()  # убираем пробелы в конце
    if len(t.value) > MAX_IDENT_LEN:
        t.value = t.value[:MAX_IDENT_LEN]
    return t

def t_NUMBER(t):
    r'\d+(?:\.\d+)?(?:[eE][+-]?\d+)?'
    t.value = float(t.value)
    return t

t_ignore = ' \t\n'

lexer = lex.lex()

if __name__ == '__main__':
    with open('input.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    lexer.input(text)
    
    for tok in lexer:
        print(f"LexToken({tok.type}, {tok.value})")

def t_error(t):
    print(f"Недопустимый символ: {t.value[0]}")
    t.lexer.skip(1)
