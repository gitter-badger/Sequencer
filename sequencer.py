from structures import *

class Sequencer():
    def __init__(self, code):
        self.code = self.parse(code)

    def parse(self, code):
        return code.split()

    def run(self, input_):
        self.input_manager = InputManager(input_)
