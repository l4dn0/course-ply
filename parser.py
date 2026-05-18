import ply.yacc as yacc
import lexer

# Токены берутся из lexer, но для yacc нужно объявить их заново
tokens = lexer.tokens

class IfNode:
    def __init__(self, assignment, cond):
        self.assignment = assignment  # оператор присваивания
        self.cond = cond              # условное выражение

class AssignNode:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

class BinOpNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class NumNode:
    def __init__(self, val):
        self.val = val

class VarNode:
    def __init__(self, name):
        self.name = name

def p_programs(p):
    '''programs : program
                | programs program'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_program(p):
    'program : if_statement'
    p[0] = p[1]

def p_if_statement(p):
    'if_statement : assignment IF condition'
    p[0] = IfNode(p[1], p[3])

def p_assignment(p):
    'assignment : ASSIGN IDENTIFIER expression SEMICOLON'
    p[0] = AssignNode(p[2], p[3])

def p_condition(p):
    '''condition : GT expression expression
                 | LT expression expression
                 | GTE expression expression
                 | LTE expression expression
                 | EQ expression expression
                 | NEQ expression expression
                 | AND condition condition'''
    if p[1] == 'and':
        p[0] = BinOpNode('and', p[2], p[3])
    else:
        p[0] = BinOpNode(p[1], p[2], p[3])

def p_expression(p):
    '''expression : NUMBER
                  | IDENTIFIER
                  | ADD expression expression
                  | SUB expression expression
                  | MUL expression expression
                  | DIV expression expression
                  | CONCAT expression expression
                  | SUBSTR expression expression
                  | LPAREN expression RPAREN'''
    if len(p) == 2:
        if type(p[1]) == float:
            p[0] = NumNode(p[1])
        else:
            p[0] = VarNode(p[1])
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = BinOpNode(p[1], p[2], p[3])

def p_error(p):
    if p:
        print(f"Синтаксическая ошибка в токене '{p.value}' (тип: {p.type})")
    else:
        print("Синтаксическая ошибка в конце файла")

# генератор c-кода
def to_c(node):
    if type(node).__name__ == 'IfNode':
        assignment = to_c(node.assignment)
        cond = to_c(node.cond)
        return f"if ({cond}) {{\n    {assignment};\n}}"
    
    if type(node).__name__ == 'AssignNode':
        return f"{node.var} = {to_c(node.expr)}"
    
    if type(node).__name__ == 'BinOpNode':
        left = to_c(node.left)
        right = to_c(node.right)
        ops = {'add':'+','sub':'-','mul':'*','div':'/',
               'eq':'==','neq':'!=','and':'&&',
               'gt':'>','lt':'<','gte':'>=','lte':'<=',
               'concat':'strcat','substr':'substr'}
        return f"({left} {ops[node.op]} {right})"
    
    if type(node).__name__ == 'NumNode':
        # Проверяем, целое ли число
        if node.val.is_integer():
            return str(int(node.val))
        return str(node.val)
    
    if type(node).__name__ == 'VarNode':
        return node.name
    
    return ""

# запуск
parser = yacc.yacc()

if __name__ == '__main__':
    with open('input.txt', 'r', encoding='utf-8') as f:
        code = f.read()
    
    print("Исходный код:")
    print(code)
    print("\n" + "="*50)
    
    # Лексический анализ для отладки
    print("\nТокены:")
    lexer.lexer.input(code)
    for tok in lexer.lexer:
        print(f"  {tok.type}: '{tok.value}'")
    
    print("\n" + "="*50)
    print("Результат парсинга:\n")
    
    ast = parser.parse(code, lexer=lexer.lexer)
    
    # ast теперь может быть списком
    if type(ast).__name__ == 'list':
        result = '\n'.join([to_c(x) for x in ast])
    else:
        result = to_c(ast)
    
    print(result)
    
    with open('output.c', 'w', encoding='utf-8') as f:
        f.write(result)

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    
    print("\n" + "="*50)
    print("Код сохранен в output.c")
