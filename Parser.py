import json

from Expression import *
from Operator import operators
from Quantifier import Quantifier


def parse_simple_primitive(spec):
    if isinstance(spec, float) or isinstance(spec, int):
        func = Primitives.create_value_func(spec)
        return Expression(spec, func, is_constant=True)

    if isinstance(spec, str):
        # func = Primitives.create_set_func(spec)
        func = Primitives.cardinality_functions[spec]
        return Expression(spec, func)

    raise ValueError('Unsupported input type {0}'.format(type(spec)))


def parse_expression(spec, setup):
    if isinstance(spec, list):
        func = operators[spec[0]].func
        arg_expressions = []
        for arg_spec in spec[1:]:
            arg_expressions.append(parse_expression(arg_spec,setup))
        return Expression(spec[0], func, *arg_expressions)

    return setup.parse_primitive(spec)


def parse_quantifiers(specs, setup):
    quantifiers = {}
    for (name, spec) in specs.items():
        if spec['presupposition'] is None:
            presupposition = None
        else:
            presupposition = parse_expression(spec['presupposition'], setup)
        quantifiers[name] = Quantifier(parse_expression(spec['expression'], setup), presupposition)
    return quantifiers


def load_from_file(filename, setup):
    with open(filename) as json_file:
        data = json.load(json_file)

    quantifier_specs = data['quantifiers']
    return parse_quantifiers(quantifier_specs, setup)
