import argparse
import codecs
import sys

from s_parser import Parser
from core import *

sys.setrecursionlimit(100000)

class Sequencer():
    def __init__(self, code):
        self.code = Parser().parser.parse(code)

    def run(self):
        env = Environment()

        for statement in self.code:
            try:
                statement.execute(env)
            except KeyboardInterrupt:
                print("^C", file=sys.stderr)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("program_path", help="Path to file containing program", type=str)

    args = arg_parser.parse_args()
    filename = args.program_path

    try:
        with open(filename) as infile:
            interpreter = Sequencer(infile.read())

    except UnicodeDecodeError:
        with codecs.open(filename, encoding="utf_8") as infile:
            interpreter = Sequencer(infile.read())

    interpreter.run()
    
