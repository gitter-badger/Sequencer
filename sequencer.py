from structures import *

import sympy

def parse(code):
    program_stack = [[]]

    for c in code:
        program_stack[-1].append(c)

    while len(program_stack) > 1:
        last = program_stack.pop()
        program_stack[-1].append(last)

    return program_stack[-1]


def evaluate(code, stack, env):
    for token in code:
        if token in "①②③④⑤⑥⑦⑧⑨⑩":
            stack.push(ExplicitInput("①②③④⑤⑥⑦⑧⑨⑩".index(token) + env.index_base))

        elif token in "0123456789":
            stack.push(Numeric(int(token)))

        elif token == "↔":
            # Swap
            elem2 = stack.pop()
            elem1 = stack.pop()

            stack.push(elem2)
            stack.push(elem1)

        elif token == "↷":
            # Move third to top
            elem3 = stack.pop()
            elem2 = stack.pop()
            elem1 = stack.pop()

            stack.push(elem2)
            stack.push(elem3)
            stack.push(elem1)

        elif token == "↶":
            # Move top to below third
            elem3 = stack.pop()
            elem2 = stack.pop()
            elem1 = stack.pop()

            stack.push(elem3)
            stack.push(elem1)
            stack.push(elem2)

        elif token in OPERATORS:
            op = OPERATORS[token]
            elems = [stack.pop() for _ in range(op.arity)][::-1]
            stack.push(op(*elems))

    return stack.pop().evaluate(env)


OPERATORS = {
    "√": VectorisedUnaryOp("Sqrt", lambda n: sympy.sqrt(n)),
    "_": VectorisedUnaryOp("Neg", lambda n: -n),
    "⌊": VectorisedUnaryOp("Floor", lambda n: sympy.floor(n)),
    "⌈": VectorisedUnaryOp("Ceil", lambda n: sympy.ceil(n)), # Need to pick a symbol for Round
    
    "+": VectorisedBinaryOp("Add", lambda m,n: m+n),
    "-": VectorisedBinaryOp("Sub", lambda m,n: m-n),
    "×": VectorisedBinaryOp("Mul", lambda m,n: m*n),
    "÷": VectorisedBinaryOp("Div", lambda m,n: m/n),
}

def floatify(elem):
    if isinstance(elem, list):
        return [floatify(x) for x in elem]

    if elem.is_integer:
        return int(elem)

    if elem.is_imaginary:
        return complex(elem)

    return float(elem)

code = parse("√_×√⌊")
env = Environment([4])
print(floatify(evaluate(code, Stack(env), env)))
