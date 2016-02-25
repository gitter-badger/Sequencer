from functools import lru_cache
import sys

import sympy

class Function():
    def __call__(self, env, args):
        env.enter_scope()
        result = self.call(env, args)
        env.exit_scope()
        return result

    def call(self, env, args):
        raise NotImplementedError

class Sequence(Function):
    def __init__(self, offset=1):
        self.offset = offset
        self.pattern_to_assignment = []


    def call(self, env, args):
        # TODO: Make it work for multiple args.
        assert len(args) == 1
        index = args[0]
        
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

                elif solution.is_integer is None:
                    sys.stderr.write("Warning: Couldn't tell whether pattern solution was integral")
                    pass

            if integer_solutions:
                # Return the smallest nonnegative solution if possible
                principal_solution = sorted(integer_solutions, key=lambda n: (0, n) if n >= 0 else (1, -n))[0]
                symbol = list(pattern.free_symbols)[0]
                env.put(str(symbol), principal_solution)
                result = assignment.evaluate(env).subs(symbol, principal_solution)
                return result

        return sympy.sympify(0)


    def add_pattern(self, pattern, assignment):
        self.pattern_to_assignment.append((pattern, assignment))


class Environment():
    def __init__(self):
        self.vars = [{
            'print': macros.s_print
        }]

    def __contains__(self, identifier):
        return self.has(identifier)

    def __getitem__(self, identifier):
        return self.get(identifier)

    def __repr__(self):
        # For debugging purposes.
        return repr(self.vars)

    def get(self, identifier):
        if identifier in self.vars[-1]:
            return self.vars[-1][identifier]

        if identifier in self.vars[0]:
            return self.vars[0][identifier]

        exit("{} not in scope".format(identifier))

    def has(self, identifier):
        return identifier in self.vars[-1] or identifier in self.vars[0]

    def put_global(self, identifier, item):
        self.vars[0][identifier] = item

    def put(self, identifier, item):
        self.vars[-1][identifier] = item

    def enter_scope(self):
        self.vars.append({})

    def exit_scope(self):
        self.vars.pop()


# TODO: Fix circular dependency.
import macros
