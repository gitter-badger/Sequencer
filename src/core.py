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


class Environment():
    def __init__(self):
        self.globals = {
            'print': macros.s_print
        }

        self.locals = [{}]

    def __contains__(self, identifier):
        return self.has(identifier)

    def __getitem__(self, identifier):
        return self.get(identifier)

    def __repr__(self):
        # For debugging purposes.
        return repr(self.globals) + "\n" + repr(self.locals)

    def get(self, identifier):
        if identifier in self.locals[-1]:
            return self.locals[-1][identifier]

        if identifier in self.globals:
            return self.globals[identifier]

        exit("{} not in scope".format(identifier))

    def has(self, identifier):
        return identifier in self.locals[-1] or identifier in self.globals

    def put_global(self, identifier, item):
        self.globals[identifier] = item

    def put_local(self, identifier, item):
        self.locals[-1][identifier] = item

    def enter_scope(self):
        self.locals.append({})

    def exit_scope(self):
        self.locals.pop()


# TODO: Fix circular dependency.
import macros
