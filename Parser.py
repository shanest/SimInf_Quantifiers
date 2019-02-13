from Expression import *
from Operator import operators
from Quantifier import Quantifier


def parse_expression(spec):
    if isinstance(spec, list):
        func = operators[spec[0]].func
        arg_expressions = []
        for arg_spec in spec[1:]:
            arg_expressions.append(parse_expression(arg_spec))
        return Expression(spec[0], func, *arg_expressions)

    if isinstance(spec, float) or isinstance(spec, int):
        func = Primitives.create_value_func(spec)
        return Expression(spec, func)

    if isinstance(spec, str):
        func = Primitives.create_set_func(spec)
        return Expression(spec, func)

    raise ValueError('Unexpected input format. Should be integer, string or list.')


def parse_quantifiers(specs):
    quantifiers = {}
    for (name, spec) in specs.items():
        if spec['presupposition'] is None:
            presupposition = None
        else:
            presupposition = parse_expression(spec['presupposition'])
        quantifiers[name] = Quantifier(parse_expression(spec['expression']), presupposition)
    return quantifiers