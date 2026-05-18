from os import write

from lexer import *
from parser import *

# =========================================================
# ГЕНЕРАЦИЯ C
# =========================================================

def to_c(node):

    if isinstance(node, IfNode):

        cond = to_c(node.cond)
        body = to_c(node.body)

        return f"if ({cond}) {{\n    {body}\n}}"

    elif isinstance(node, AssignNode):

        var = to_c(node.var)
        expr = to_c(node.expr)

        return f"{var} = {expr};"


    elif isinstance(node, BinOpNode):

        left = to_c(node.left)

        # квадрат
        if node.op == '^':
            return f"({left} * {left})"

        right = to_c(node.right)

        return f"({left} {node.op} {right})"


    elif isinstance(node, NumberNode):

        return str(node.value)


    elif isinstance(node, VariableNode):

        if node.index is not None:
            return f"{node.name.strip()}[{node.index}]"

        return node.name.strip()

# =========================================================
# КОМПИЛЯЦИЯ
# =========================================================

def compile_code(source):

    lexer.lineno = 1

    ast = parser.parse(source, lexer=lexer)

    if not ast:
        return ""

    return '\n'.join(to_c(x) for x in ast)

if __name__ == "__main__":
    with open('input.txt', 'r') as file:
        tests = file.read().split('\n')
        print(tests)

    # tests = [
    #     "x > 07 ? := x x - 01 ;",
    #     "x > 01 ? y < 07 ? := y y - 01 ;",
    #     "x == 01 ? := y y^ ;",
    #     "flag[03] != 00 ? := x x - 01 ;",
    #     "x > 077 ? := x x - 010 ;",
    #     "flag[07] != 00 ? x > 010 ? := y (y - 01)^ ;",
    # ]

    for code in tests:

        print("\n================================")
        print("Ввод:")
        print(code)

        result = compile_code(code)

        print("\nВывод на языке C:")
        print(result)
        with open(f"output.txt", 'a') as file:
            print(result)
            print(result + "\n", file=file)

    print("Результат сохранён в файл output.txt")