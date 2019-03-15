import json
from os import path
from pydoc import locate

import Generator
import Measurer
import Operator
import Parser


class ExperimentSetup(object):

    def __init__(self, name, lexical_quantifiers_filename, model_generator, primitive_generator, primitive_parser, expression_complexity_measurer, quantifier_complexity_measurer, operators):
        self.name = name
        self.lexical_quantifiers_filename = lexical_quantifiers_filename
        self.generate_models = model_generator
        self.generate_primitives = primitive_generator
        self.operators = {name: Operator.operators[name] for name in operators}
        self.parse_primitive = primitive_parser
        self.measure_expression_complexity = expression_complexity_measurer
        self.measure_quantifier_complexity = quantifier_complexity_measurer

        self.possible_input_types = []
        for (name, operator) in self.operators.items():
            self.possible_input_types.append(operator.inputTypes)


def parse(filename):
    with open(filename) as file:
        props = json.load(file)

    return ExperimentSetup(
        props['name'],
        path.join(path.dirname(filename),props['lexical_quantifiers_filename']),
        locate(props['model_generator']),
        locate(props['primitive_generator']),
        locate(props['primitive_parser']),
        locate(props['expression_complexity_measurer']),
        locate(props['quantifier_complexity_measurer']),
        props['operators']
    )


setup_1 = ExperimentSetup(
    'Setup1',
    'EnglishQuantifiers_Setup1.json',
    Generator.generate_simplified_models,
    Generator.generate_simple_primitive_expressions,
    Parser.parse_simple_primitive,
    Measurer.measure_expression_complexity,
    Measurer.measure_complexity,
    [">f", ">", ">=", "=", "/", "and", "or", "not"]
)

setup_2 = ExperimentSetup(
    'Setup2',
    'EnglishQuantifiers_Setup2.json',
    Generator.generate_simplified_models,
    Generator.generate_simple_primitive_expressions_with_sets,
    Parser.parse_simple_primitive_with_sets,
    Measurer.measure_expression_complexity,
    Measurer.measure_complexity,
    [">f", ">", ">=", "=", "/", "and", "or", "not", "subset", "intersection", "union", "card", "diff", "empty"]
)