import itertools

import sympy

class Evaluable():
    def evaluate(self, env):
        raise NotImplementedError


class NullaryOp(Evaluable):
    arity = 0


class ImplicitInput(NullaryOp):
    def __init__(self, number):
        self.number = sympy.sympify(number)

    def evaluate(self, env):
        return env.input_num(self.number)

    def __repr__(self):
        return "ImplicitInput({})".format(self.number)


class ExplicitInput(NullaryOp):
    """①②③④⑤⑥⑦⑧⑨⑩: input"""
    def __init__(self, number):
        self.number = number

    def evaluate(self, env):
        if (env.index_base <= self.number < env.index_base + len(env.inputs)):
            return env.input_num(self.number)

        else:
            raise NotImplementedError

    def __repr__(self):
        return "ExplicitInput({})".format(self.number)


class Numeric(NullaryOp):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

    def __repr__(self):
        return "Numeric({})".format(self.value)


class FiniteList(NullaryOp):
    def __init__(self, list_):
        self.list = list_

    def evaluate(self, env):
        return [item.evaluate(env) for item in self.list]

    def __repr__(self):
        return "FiniteList({})".format(", ".join(map(str, self.list)))


class UnaryOp(Evaluable):
    arity = 1


class _VectorisedUnaryOp(UnaryOp):
    def __init__(self, func, child):
        self.func = func
        self.child = child

    def evaluate(self, env):
        child = self.child.evaluate(env)

        if isinstance(child, list):
            return [self.func(x) for x in child]

        return self.func(child)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.child)


def VectorisedUnaryOp(name, func):
    def __init__(self, child):
        _VectorisedUnaryOp.__init__(self, func, child)

    new_class = type(name, (_VectorisedUnaryOp,), {"__init__": __init__})
    return new_class


class BinaryOp(Evaluable):
    arity = 2


class _VectorisedBinaryOp(BinaryOp):
    def __init__(self, func, left, right):
        self.func = func
        self.left = left
        self.right = right

    def evaluate(self, env):
        left = self.left.evaluate(env)
        right = self.right.evaluate(env)

        if isinstance(left, list) and isinstance(right, list):
            result = []

            for a, b in itertools.zip_longest(left, right):
                if a is None:
                    result.append(b)
                elif b is None:
                    result.append(a)
                else:
                    result.append(self.func(a, b))

            return result

        elif isinstance(left, list):
            return [self.func(x, right) for x in left]

        elif isinstance(right, list):
            return [self.func(left, y) for y in right]

        return self.func(left, right)


    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, self.left, self.right)


def VectorisedBinaryOp(name, func):
    def __init__(self, left, right):
        _VectorisedBinaryOp.__init__(self, func, left, right)

    new_class = type(name, (_VectorisedBinaryOp,), {"__init__": __init__})
    return new_class
