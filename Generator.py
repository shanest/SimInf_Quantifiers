import itertools
from copy import deepcopy, copy

from pathos.pools import ProcessPool

from GeneralizedQuantifierModel import *
from itertools import chain, combinations
from Expression import *
import numpy as np

from Quantifier import Quantifier
from SetPlaceholders import SetPlaceholder


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
    expressions = {int: [], float: [], bool: [], SetPlaceholder: []}

    for i in range(0, max_integer+1, 5):
        expressions[int].append(Expression(i, Primitives.create_value_func(i), is_constant=True))

    for set_name in ['A', 'B', 'A-B', 'A&B']:
        expressions[int].append(Expression(set_name, Primitives.cardinality_functions[set_name]))

    for q in np.arange(0, 1, .1):
        expressions[float].append(Expression(q, Primitives.create_value_func(q), is_constant=True))

    for boolean in [True, False]:
        expressions[bool].append(Expression(boolean, Primitives.create_value_func(boolean), is_constant=True))

    return expressions


def generate_simple_primitive_expressions_with_sets(max_integer):
    expressions = {int: [], float: [], bool: [], SetPlaceholder: []}

    for i in range(0, max_integer+1, 5):
        expressions[int].append(Expression(i, Primitives.create_value_func(i), is_constant=True))

    for set_name in ['A', 'B']:
        expressions[SetPlaceholder].append(
            Expression(set_name, Primitives.create_value_func(SetPlaceholder(set_name)))
        )

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
        SetPlaceholder: {}
    }

    return clean_expressions({1:expressions}, expressions_by_meaning, 1, universe)


def calculate_arg_length_options(arg_amount, total_length):
    if arg_amount == 1:
        return [[total_length]]

    options = []
    for last_arg_length in range(1,total_length-arg_amount+2):
        for smaller_option in calculate_arg_length_options(arg_amount-1,total_length-last_arg_length):
            smaller_option.append(last_arg_length)
            options.append(smaller_option)

    return options


def generate_all_expressions(setup, max_length, max_integer, universe, boolean=True):
    if max_length is 1:
        return generate_all_primitive_expressions(setup,max_integer,universe)

    (smaller_expressions, expressions_by_meaning) = generate_all_expressions(setup, max_length-1, max_integer, universe, False)

    arg_length_options = {amount: calculate_arg_length_options(amount,max_length-1) for amount in range(2,4)}

    arg_options_by_types = {}

    for inputTypes in setup.possible_input_types:
        if isinstance(inputTypes, type):
            arg_options_by_types[inputTypes] = [[arg] for arg in smaller_expressions[max_length-1][inputTypes]]

        else:
            arg_options = []
            for arg_lengths in arg_length_options[len(inputTypes)]:
                arg_lists = []
                for (arg_length,inputType) in zip(arg_lengths,inputTypes):
                    arg_lists.append(smaller_expressions[arg_length][inputType])
                arg_options.extend(itertools.product(*arg_lists))

            arg_options_by_types[inputTypes] = arg_options

    expressions = smaller_expressions
    expressions[max_length] = {}

    for returnType in [bool, int, float, SetPlaceholder]:
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

    for type in [bool, int, float, SetPlaceholder]:
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


def merge_meanings(presup_meaning, expr_meaning):
    return tuple([e if p else None for (p, e) in zip(presup_meaning, expr_meaning)])


def add_presuppositions(setup, expressions_by_meaning):

    quantifiers_by_meaning = {meaning: Quantifier(expression) for (meaning,expression) in expressions_by_meaning.items()}

    for (e_meaning, expression) in expressions_by_meaning.items():
        for (p_meaning, presupposition) in expressions_by_meaning.items():
            meaning = merge_meanings(p_meaning, e_meaning)
            if True not in meaning or False not in meaning:
                continue
            quantifier = Quantifier(expression,presupposition)

            if meaning in quantifiers_by_meaning.keys():
                other_quantifier = quantifiers_by_meaning[meaning]

                this_complexity = setup.measure_quantifier_complexity(quantifier)
                other_complexity = setup.measure_quantifier_complexity(other_quantifier)
                if this_complexity >= other_complexity:
                    continue

            quantifiers_by_meaning[meaning] = quantifier

    return quantifiers_by_meaning