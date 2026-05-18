from ply import yacc
from lexer import *

# =========================================================
# ПАРСЕР
# =========================================================

def p_program(p):
    '''
    program : statements
    '''
    p[0] = p[1]

# ---------------------------------------------------------

def p_statements(p):
    '''
    statements : statement
               | statements statement
    '''

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# ---------------------------------------------------------

def p_statement(p):
    '''
    statement : if_statement SEMICOLON
    '''
    p[0] = p[1]

# ---------------------------------------------------------
# Вложенные сокращенные условные операторы
# condition ? operator
# ---------------------------------------------------------

def p_if_statement_assign(p):
    '''
    if_statement : condition QUESTION assign_statement
    '''
    p[0] = IfNode(p[1], p[3])

# ---------------------------------------------------------

def p_if_statement_nested(p):
    '''
    if_statement : condition QUESTION if_statement
    '''
    p[0] = IfNode(p[1], p[3])

# ---------------------------------------------------------
# Присваивание
# := x expr
# ---------------------------------------------------------

def p_assign_statement(p):
    '''
    assign_statement : ASSIGN variable expression
    '''
    p[0] = AssignNode(p[2], p[3])

# ---------------------------------------------------------
# Условия
# ---------------------------------------------------------

def p_condition(p):
    '''
    condition : expression EQ expression
              | expression NEQ expression
              | expression LT expression
              | expression GT expression
    '''

    p[0] = BinOpNode(p[2], p[1], p[3])

# ---------------------------------------------------------
# Вычитание
# ---------------------------------------------------------

def p_expression_minus(p):
    '''
    expression : expression MINUS expression
    '''
    p[0] = BinOpNode('-', p[1], p[3])

# ---------------------------------------------------------
# Возведение в квадрат
# postfix
# x^
# ---------------------------------------------------------

def p_expression_square(p):
    '''
    expression : expression POWER
    '''
    p[0] = BinOpNode('^', p[1])

# ---------------------------------------------------------

def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

# ---------------------------------------------------------

def p_expression_number(p):
    '''
    expression : NUMBER
    '''
    p[0] = NumberNode(p[1])

# ---------------------------------------------------------

def p_expression_variable(p):
    '''
    expression : variable
    '''
    p[0] = p[1]

# ---------------------------------------------------------
# Переменные
# ---------------------------------------------------------

def p_variable_simple(p):
    '''
    variable : IDENTIFIER
    '''
    p[0] = VariableNode(p[1])

# ---------------------------------------------------------

def p_variable_indexed(p):
    '''
    variable : IDENTIFIER LBRACKET NUMBER RBRACKET
    '''
    p[0] = VariableNode(p[1], p[3])

# ---------------------------------------------------------

def p_error(p):

    if p:
        print(
            f"Синтаксическая ошибка "
            f"в токене '{p.value}' "
            f"(тип {p.type}) "
            f"строка {p.lineno}"
        )
    else:
        print("Синтаксическая ошибка в конце файла")

# ---------------------------------------------------------

parser = yacc.yacc()