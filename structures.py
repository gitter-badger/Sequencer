class InputManager():
    def __init__(self, inputs_):
        self.inputs = inputs_
        self.index = 1

    def __getitem__(self, index):
        if self.inputs:
            return self.inputs[(index-1) % len(self.inputs)]
        else:
            return 0

    def __next__(self):
        result = self[self.index]
        self.index += 1

        if self.index > len(self.inputs):
            self.index = 1

        return result


class Stack():
    def __init__(self, input_manager):
        self.stack = []
        self.input_manager = input_manager

    def push(self, elem):
        self.stack.append(elem)

    def pop(self):
        if self.stack:
            return self.stack.pop()

        return next(input_manager)
