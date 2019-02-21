from copy import deepcopy, copy

from pathos.pools import ProcessPool

from GeneralizedQuantifierModel import *
from itertools import chain, combinations, product
from Expression import *
import random
import numpy as np
from Operator import operatorsByReturnType, possibleInputTypes, operators
import Generator
import Measurer
from Quantifier import Quantifier


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def generate_models(size):
    M = set(range(size))
    M_powerset = list(powerset(M))
    models = []
    for A in M_powerset:
        for B in M_powerset:
            models.append(GeneralizedQuantifierModel(M, set(A), set(B)))
    return models

def generate_simplified_models(size):
    models = []
    for AminusB in range(size+1):
        for AandB in range(size+1-AminusB):
            for BminusA in range(size+1-AminusB-AandB):
                models.append(SimplifiedQuantifierModel(AminusB+AandB,BminusA+AandB,AminusB,AandB))
    return models


def generate_primitive_expression(return_type, max_integer):
    if return_type == int:
        if random.random() < .5:
            x = random.choice(range(max_integer))
            return Expression(x, Primitives.create_value_func(x))
        else:
            x = random.choice(['A', 'B', 'A-B', 'A&B'])
            return Expression(x, Primitives.cardinality_functions[x])
    if return_type == float:
        q = random.choice(np.arange(0, 1, .1))
        return Expression(q, Primitives.create_value_func(q))
    if return_type == set:
        set_name = random.choice(['A', 'B'])
        return Expression(set_name, Primitives.create_set_func(set_name))
    if return_type == bool:
        boolean = random.choice([True, False])
        return Expression(boolean, Primitives.create_value_func(boolean))
    raise ValueError('Return type must be int, float, set or bool.')


def generate_expression(return_type, size, max_integer):
    if size == 0:
        return generate_primitive_expression(return_type, max_integer)

    (name, operator) = random.choice(operatorsByReturnType[return_type])

    arg_expressions = []
    size_left = size-1
    for (i,arg_type) in enumerate(operator.inputTypes):
        if i+1 is len(operator.inputTypes):
            arg_size = size_left
        else:
            arg_size = random.choice(range(size_left)) if size_left > 0 else 0
        size_left -= arg_size
        arg_expressions.append(generate_expression(arg_type, arg_size, max_integer))

    return Expression(name, operator.func, *arg_expressions)


def generate_unique_quantifiers(lengths, amount_per_length, presupposition_lengths, amount_per_length_combination, max_integer, universe):
    generated_quantifier_by_meaning = {}

    QuantifierBlueprint = namedtuple("QuantifierBlueprint", "expression_length presupposition_length amount")
    blueprints = [QuantifierBlueprint(expression_length, presupposition_length, amount_per_length_combination)
                  for (expression_length, presupposition_length) in product(lengths, presupposition_lengths)]

    leftover = amount_per_length - (amount_per_length_combination * len(presupposition_lengths))
    blueprints.extend(QuantifierBlueprint(length, 0, leftover) for length in lengths)

    for blueprint in blueprints:
        print("Start generating length {0},{1}".format(blueprint.presupposition_length, blueprint.expression_length))
        for i in range(blueprint.amount):
            new_better_expression = False
            while not new_better_expression:
                expression = Generator.generate_expression(bool, blueprint.expression_length, max_integer)
                presupposition = Generator.generate_expression(bool, blueprint.presupposition_length, max_integer)\
                    if blueprint.presupposition_length > 0 else None

                quantifier = Quantifier(expression, presupposition)

                meaning = tuple([quantifier.evaluate(model) for model in universe])

                if False not in meaning or True not in meaning:
                    continue

                if meaning in generated_quantifier_by_meaning.keys():
                    other_quantifier = generated_quantifier_by_meaning[meaning]

                    this_complexity = Measurer.measure_complexity(quantifier)
                    other_complexity = Measurer.measure_complexity(other_quantifier)
                    if this_complexity > other_complexity:
                        continue

                generated_quantifier_by_meaning[meaning] = quantifier
                new_better_expression = True

    return list(generated_quantifier_by_meaning.values()), list(generated_quantifier_by_meaning.keys())


def generate_all_primitive_expressions(max_integer, universe):
    expressions = {int: [], float: [], bool: []}

    for i in range(0, max_integer+1, 5):
        expressions[int].append(Expression(i, Primitives.create_value_func(i), is_constant=True))

    for set_name in ['A', 'B', 'A-B', 'A&B']:
        expressions[int].append(Expression(set_name, Primitives.cardinality_functions[set_name]))

    for q in np.arange(0, 1, .1):
        expressions[float].append(Expression(q, Primitives.create_value_func(q), is_constant=True))

    for boolean in [True, False]:
        expressions[bool].append(Expression(boolean, Primitives.create_value_func(boolean), is_constant=True))

    expressions_by_meaning = {
        bool: {},
        int: {},
        float: {}
    }

    return clean_expressions({1:expressions}, expressions_by_meaning,1,universe)


def generate_all_expressions(max_length, max_integer, universe, boolean=True):
    if max_length is 1:
        return generate_all_primitive_expressions(max_integer,universe)

    (smaller_expressions, expressions_by_meaning) = generate_all_expressions(max_length-1, max_integer, universe, False)

    arg_length_options = [(a, max_length - 1 - a) for a in range(1, max_length - 1)]

    arg_options_by_types = {}

    for inputTypes in possibleInputTypes:
        if isinstance(inputTypes, type):
            arg_options_by_types[inputTypes] = [[arg] for arg in smaller_expressions[max_length-1][inputTypes]]

        else:
            arg_options = []
            for arg_lengths in arg_length_options:
                for arg0 in smaller_expressions[arg_lengths[0]][inputTypes[0]]:
                    for arg1 in smaller_expressions[arg_lengths[1]][inputTypes[1]]:
                        arg_options.append([arg0,arg1])
            arg_options_by_types[inputTypes] = arg_options

    expressions = smaller_expressions
    expressions[max_length] = {}

    for returnType in operatorsByReturnType.keys():
        expressions[max_length][returnType] = []

    for (name,operator) in operators.items():
        for args in arg_options_by_types[operator.inputTypes]:
            expressions[max_length][operator.outputType].append(Expression(name, operator.func, *args))

    print('Finished step {0}, cleaning'.format(max_length))
    return clean_expressions(expressions, expressions_by_meaning, max_length, universe)


class MeaningCalculator(object):
    def __init__(self, universe):
        self.universe = universe

    def __call__(self, expression):
        return tuple(expression.evaluate(model) for model in self.universe)


def clean_expressions(expressions, expressions_by_meaning, length, universe):

    for type in [bool, int, float]:
        print('cleaning {0} {1}s'.format(len(expressions[length][type]),str(type)))
        p = ProcessPool(nodes=4)
        new_meanings = p.map(MeaningCalculator(universe), expressions[length][type])

        new_expressions = copy(expressions[length][type])
        for (expression, meaning) in zip(new_expressions, new_meanings):
            if meaning in expressions_by_meaning[type].keys():
                other_expression = expressions_by_meaning[type][meaning]

                this_complexity = expression.length()
                other_complexity = other_expression.length()
                if this_complexity >= other_complexity:
                    expressions[length][type].remove(expression)
                    continue
                else:
                    expressions[other_expression.length()][type].remove(other_expression)

            expressions_by_meaning[type][meaning] = expression

        print('{0} were clean'.format(len(expressions[length][type])))

    print('Finished cleaning step {0}'.format(length))
    return expressions, expressions_by_meaning
