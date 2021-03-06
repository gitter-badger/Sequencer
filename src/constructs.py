import sympy

from core import *
from error_templates import *

class Expression():
    def evaluate(self, env):
        raise NotImplementedError


class Statement():
    def execute(self, env):
        raise NotImplementedError


class SequenceAssignment(Statement):
    def __init__(self, variable, pattern, assignment):
        self.identifier = variable.identifier
        self.pattern = pattern
        self.assignment = assignment

    def execute(self, env):
        if self.identifier in env:
            sequence = env.get(self.identifier)

            if not isinstance(sequence, Sequence):
                exit("{} is not a sequence".format(self.identifier))
        else:
            sequence = Sequence()
            env.put(self.identifier, sequence)

        sequence.add_pattern(self.pattern, self.assignment)


class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def execute(self, env):
        self.expression.evaluate(env)


class Number(Expression):
    def __init__(self, value):
        self.value = sympy.sympify(value)

    def __repr__(self):
        return str(self.value)

    def evaluate(self, env):
        return self.value


class Variable(Expression):
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return str(self.identifier)

    def evaluate(self, env):
        if self.identifier in env:
            return env[self.identifier]
        else:
            return sympy.Symbol(self.identifier)


class UnaryOp(Expression):
    def __init__(self, child, func):
        self.child = child
        self.func = func

    def evaluate(self, env):
        return self.func(self.child.evaluate(env))


class BinaryOp(Expression):
    def __init__(self, left, right, func):
        self.left = left
        self.right = right        
        self.func = func

    def evaluate(self, env):
        return self.func(self.left.evaluate(env), self.right.evaluate(env))
        

class FunctionCall(Expression):
    def __init__(self, caller, args):
        self.caller = caller
        self.args = args

    def evaluate(self, env):
        caller = self.caller.evaluate(env)

        if isinstance(caller, sympy.Symbol):
            exit(NOT_DEFINED.format(self.identifier))

        args = [x.evaluate(env) for x in self.args]
        return caller(env, args)
