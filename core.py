from functools import lru_cache
import sys

import sympy

class Sequence():
    def __init__(self, offset=1):
        self.offset = offset
        self.pattern_to_assignment = []


    def __call__(self, env, index):
        if isinstance(index, list):
            index = index[0]

        # Reverse since we want later patterns to take priority
        for pattern, assignment in reversed(self.pattern_to_assignment):
            try:
                pattern = pattern.evaluate(env)
            except ValueError:
                exit("Invalid pattern")

            if len(pattern.free_symbols) > 1:
                exit("Invalid pattern")

            if len(pattern.free_symbols) == 0:
                if pattern.equals(index):
                    return assignment.evaluate(env)
                else:
                    continue

            solutions = sympy.solve(sympy.Eq(pattern, index))
            integer_solutions = []

            for solution in solutions:
                if solution.is_integer:
                    integer_solutions.append(solution)

                elif solution is None:
                    # TODO: Handle this case.
                    pass

            if integer_solutions:
                # Return the smallest nonnegative solution if possible
                result = assignment.evaluate(env).subs('n',
                          sorted(integer_solutions, key=lambda n: (0, n) if n >= 0 else (1, -n))[0])
                return result

        return sympy.sympify(0)


    def add_pattern(self, pattern, assignment):
        self.pattern_to_assignment.append((pattern, assignment))


class Environment(dict):
    def __init__(self):
        super().__init__({
            'print': macros.s_print
        })


    def get_sequence(self, variable):
        if variable.identifier in self:
            elem = self[variable.identifier]

            if isinstance(elem, Sequence):
                return elem
            else:
                raise TypeError("'{}' is not of type 'Sequence'".format(identifier))

        else:
            self[variable.identifier] = Sequence()
            return self[variable.identifier]


# TODO: Fix circular dependency.
import macros
