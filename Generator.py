from copy import deepcopy, copy

from pathos.pools import ProcessPool

from GeneralizedQuantifierModel import *
from itertools import chain, combinations
from Expression import *
import numpy as np


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


def generate_simple_primitive_expressions(max_integer):
    expressions = {int: [], float: [], bool: [], set: []}

    for i in range(0, max_integer+1, 5):
        expressions[int].append(Expression(i, Primitives.create_value_func(i), is_constant=True))

    for set_name in ['A', 'B', 'A-B', 'A&B']:
        expressions[int].append(Expression(set_name, Primitives.cardinality_functions[set_name]))

    for q in np.arange(0, 1, .1):
        expressions[float].append(Expression(q, Primitives.create_value_func(q), is_constant=True))

    for boolean in [True, False]:
        expressions[bool].append(Expression(boolean, Primitives.create_value_func(boolean), is_constant=True))

    return expressions


def generate_all_primitive_expressions(setup, max_integer, universe):
    expressions = setup.generate_primitives(max_integer)

    expressions_by_meaning = {
        bool: {},
        int: {},
        float: {},
        set: {}
    }

    return clean_expressions({1:expressions}, expressions_by_meaning, 1, universe)


def generate_all_expressions(setup, max_length, max_integer, universe, boolean=True):
    if max_length is 1:
        return generate_all_primitive_expressions(setup,max_integer,universe)

    (smaller_expressions, expressions_by_meaning) = generate_all_expressions(setup, max_length-1, max_integer, universe, False)

    arg_length_options = [(a, max_length - 1 - a) for a in range(1, max_length - 1)]

    arg_options_by_types = {}

    for inputTypes in setup.possible_input_types:
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

    for returnType in [bool, int, float, set]:
        expressions[max_length][returnType] = []

    for (name, operator) in setup.operators.items():
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

    for type in [bool, int, float, set]:
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
