import itertools
import json

from Expression import *
from Operator import operators
from Quantifier import Quantifier
from SetPlaceholders import SetPlaceholder
import numpy as np


def parse_simple_primitive(spec):
    if isinstance(spec, float) or isinstance(spec, int):
        func = Primitives.create_value_func(spec)
        return Expression(spec, func, is_constant=True)

    if isinstance(spec, str):
        func = Primitives.cardinality_functions[spec]
        return Expression(spec, func)

    raise ValueError('Unsupported input type {0}'.format(type(spec)))


def parse_simple_primitive_with_sets(spec):
    if isinstance(spec, float) or isinstance(spec, int):
        func = Primitives.create_value_func(spec)
        return Expression(spec, func, is_constant=True)

    if isinstance(spec, str):
        func = Primitives.create_value_func(SetPlaceholder(spec))
        return Expression(spec, func)


def parse_expression(spec, setup):
    if isinstance(spec, list):
        func = operators[spec[0]].func
        arg_expressions = []
        for arg_spec in spec[1:]:
            arg_expressions.append(parse_expression(arg_spec,setup))
        return Expression(spec[0], func, *arg_expressions)

    return setup.parse_primitive(spec)


def parse_expression_options(spec, model_size):
    if isinstance(spec, list):
        func = operators[spec[0]].func
        arg_expressions_options = []
        for arg_spec in spec[1:]:
            arg_expressions_options.append(parse_expression_options(arg_spec, model_size))
        arg_options = itertools.product(*arg_expressions_options)
        return [Expression(spec[0], func, *arg_expressions) for arg_expressions in arg_options]

    return parse_primitive_options(spec, model_size)


def parse_primitive_options(spec, model_size):
    if isinstance(spec, float) or isinstance(spec, int):
        func = Primitives.create_value_func(spec)
        return [Expression(spec, func, is_constant=True)]

    if isinstance(spec, str):
        if spec == "n":
            expressions = []
            for i in range(0, model_size + 1):
                func = Primitives.create_value_func(i)
                expressions.append(Expression(str(i), func))
            return expressions
        if spec == "f":
            expressions = []
            for q in np.arange(0, 1, .1):
                func = Primitives.create_value_func(q)
                expressions.append(Expression(str(q), func))
            return expressions

        func = Primitives.create_value_func(SetPlaceholder(spec))
        return [Expression(spec, func)]


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
