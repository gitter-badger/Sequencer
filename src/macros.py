import sympy

from core import *
from error_templates import *

def s_print(env, args):
    for arg in args:
        if isinstance(arg, Sequence):
            i = arg.offset

            while True:
                print(normalise_output(arg(env, [i])))
                i += 1

        else:
            print(normalise_output(arg))


def normalise_output(elem):
    if isinstance(elem, sympy.Symbol):
        exit(NOT_DEFINED.format(elem.name))

    if isinstance(elem, list):
        return "[{}]".format(" ".join(map(normalise_output, elem)))

    if elem.is_integer:
        # TODO: Check for None.
        return int(elem)

    try:
        return float(elem)
    except TypeError:
        return complex(elem)
