from collections import namedtuple

import Generator
import Measurer
import Operator
import Parser


class ExperimentSetup(object):

    def __init__(self, name, lexical_quantifiers_filename, model_generator, primitive_generator, primitive_parser, expression_complexity_measurer, operators):
        self.name = name
        self.lexical_quantifiers_filename = lexical_quantifiers_filename
        self.generate_models = model_generator
        self.generate_primitives = primitive_generator
        self.operators = {name: Operator.operators[name] for name in operators}
        self.parse_primitive = primitive_parser
        self.expression_complexity_measurer = expression_complexity_measurer

        self.possible_input_types = []
        for (name, operator) in self.operators.items():
            self.possible_input_types.append(operator.inputTypes)


setup_1 = ExperimentSetup(
    'Setup1',
    'EnglishQuantifiers_Setup1.json',
    Generator.generate_simplified_models,
    Generator.generate_simple_primitive_expressions,
    Parser.parse_simple_primitive,
    Measurer.measure_expression_complexity,
    [">f", ">", ">=", "=", "/", "and", "or", "not"]
)