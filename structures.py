from macros import *

class Environment():
    def __init__(self, inputs_):
        self.index_base = 1
        self.inputs = inputs_

    def input_num(self, number):
        if not self.inputs:
            return 0

        index = (number - self.index_base) % len(self.inputs)
        return self.inputs[index]

    def to_sequencer(self, elem):
        if isinstance(elem, list):
            return FiniteList([self.to_sequencer(x) for x in elem])
        else:
            return Numeric(elem)


class Stack():
    def __init__(self, env):
        self.stack = []
        self.env = env
        self.input_number_offset = 0

    def push(self, elem):
        self.stack.append(elem)

    def pop(self):
        if self.stack:
            return self.stack.pop()

        result = ImplicitInput(self.input_number_offset + self.env.index_base)
        self.input_number_offset += 1
        return result

    def __repr__(self):
        return repr(self.stack)
