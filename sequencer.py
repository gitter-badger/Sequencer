from structures import *

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

        elif token in OPERATORS:
            op = OPERATORS[token]
            elems = [stack.pop() for _ in range(op.arity)]
            stack.push(op(*elems))

    return stack.pop().evaluate(env)


OPERATORS = {
    "+": VectorisedBinaryOp("Add", lambda m,n: m+n),
    "-": VectorisedBinaryOp("Sub", lambda m,n: m-n),
    "×": VectorisedBinaryOp("Mul", lambda m,n: m*n),
    "÷": VectorisedBinaryOp("Div", lambda m,n: m/n),
}

code = parse("723+×")
env = Environment([[3, 4, 5, 6], [1, 2, 3]])
print(evaluate(code, Stack(env), env))
