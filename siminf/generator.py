import itertools
from copy import copy

from siminf.generalized_quantifier_model import *

from itertools import chain, combinations

from siminf.expression import * 

import numpy as np

from siminf.quantifier import Quantifier 
from siminf.set_place_holders import SetPlaceholder  

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

    for i in range(0, max_integer+1, 2):
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

    for i in range(0, max_integer+1, 2):
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


def calculate_arg_length_options(arg_amount, total_length):
    if arg_amount == 1:
        return [[total_length]]

    options = []
    for last_arg_length in range(1,total_length-arg_amount+2):
        for smaller_option in calculate_arg_length_options(arg_amount-1,total_length-last_arg_length):
            smaller_option.append(last_arg_length)
            options.append(smaller_option)

    return options


class MeaningCalculator(object):
    def __init__(self, universe):
        self.universe = universe

    def __call__(self, expression):
        return tuple(expression.evaluate(model) for model in self.universe)


class ExpressionGenerator(object):

    def __init__(self, setup, max_integer, universe, processpool):
        self.setup = setup
        self.max_integer = max_integer
        self.universe = universe
        self.processpool = processpool

    def generate_all_primitive_expressions(self):
        expressions = self.setup.generate_primitives(self.max_integer)

        expressions_by_meaning = {
            bool: {},
            int: {},
            float: {},
            SetPlaceholder: {}
        }

        return self.clean_expressions({1: expressions}, expressions_by_meaning, 1)

    def generate_all_expressions(self, max_length):
        if max_length is 1:
            return self.generate_all_primitive_expressions()

        (smaller_expressions, expressions_by_meaning) = self.generate_all_expressions(max_length-1)

        arg_length_options = {amount: calculate_arg_length_options(amount,max_length-1) for amount in range(2,4)}

        arg_options_by_types = {}

        for inputTypes in self.setup.possible_input_types:
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

        for (name, operator) in self.setup.operators.items():
            for args in arg_options_by_types[operator.inputTypes]:
                expressions[max_length][operator.outputType].append(Expression(name, operator.func, *args))

        print('Finished step {0}, cleaning'.format(max_length))
        return self.clean_expressions(expressions, expressions_by_meaning, max_length)

    def clean_expressions(self, expressions, expressions_by_meaning, length):
        for type in [bool, int, float, SetPlaceholder]:
            print('cleaning {0} {1}s'.format(len(expressions[length][type]),str(type)))
            new_meanings = self.processpool.map(MeaningCalculator(self.universe), expressions[length][type])

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


class PresuppositionMerger(object):

    def __init__(self, setup, processpool, chunk_size):
        self.setup = setup
        self.processpool = processpool
        self.chunk_size = chunk_size

    def add_presuppositions(self, expressions_by_meaning):
        expressions = expressions_by_meaning.values()
        exp_meanings = expressions_by_meaning.keys()

        presuppositions = iter(expressions)
        presup_meanings = iter(exp_meanings)

        quantifiers = []
        meanings = []

        while True:
            presup_chunk = list(itertools.islice(presuppositions, self.chunk_size))
            presup_meaning_chunk = itertools.islice(presup_meanings, self.chunk_size)

            if len(presup_chunk) == 0:
                break

            new_quantifiers, new_meanings = self.merge_presupposition_chunk(
                expressions,
                exp_meanings,
                presup_chunk,
                presup_meaning_chunk
            )

            quantifiers.extend(new_quantifiers)
            meanings.extend(new_meanings)

        quantifiers_by_meaning = {meaning: quantifier for (meaning, quantifier)
                                  in zip(meanings, quantifiers)}
        for (exp,meaning) in zip(expressions,exp_meanings):
            quantifiers_by_meaning[meaning] = Quantifier(exp)

        return quantifiers_by_meaning

    def merge_presupposition_chunk(self, expressions, exp_meanings, presuppositions, presup_meanings):
        meanings = self.processpool.map(merge_meanings, *zip(*itertools.product(exp_meanings, presup_meanings)))

        unique_meanings = set(meanings)
        unique_meanings.remove(None)
        unique_meanings = list(unique_meanings)

        print('Filtering {0} qs down to {1}'.format(len(meanings), len(unique_meanings)))

        quantifier_list_by_meaning = {meaning: [] for meaning in unique_meanings}
        quantifiers = [Quantifier(e, p) for (e, p) in itertools.product(expressions, presuppositions)]

        for (quantifier, meaning) in zip(quantifiers, meanings):
            if meaning is not None:
                quantifier_list_by_meaning[meaning].append(quantifier)

        find_least_complex = ComplexitySorter(self.setup.measure_quantifier_complexity)
        best_quantifiers = self.processpool.map(find_least_complex, quantifier_list_by_meaning.values())

        return best_quantifiers, quantifier_list_by_meaning.keys()


class ComplexitySorter(object):

    def __init__(self, measure_function):
        self.measure_function = measure_function

    def __call__(self, quantifiers):
        if len(quantifiers) is 1:
            return quantifiers[0]

        sorted_quantifiers = sorted(quantifiers, key=lambda q: self.measure_function(q))
        return sorted_quantifiers[0]


def merge_meanings(expr_meaning, presup_meaning):
    if False not in presup_meaning:
        return None

    result = tuple(e if p else None for (p, e) in zip(presup_meaning, expr_meaning))
    if False not in result or True not in result:
        return None
    return result


def add_presuppositions(setup, expressions_by_meaning):

    quantifiers_by_meaning = {meaning: Quantifier(expression) for (meaning,expression) in expressions_by_meaning.items()}

    for (e_meaning, expression) in expressions_by_meaning.items():
        for (p_meaning, presupposition) in expressions_by_meaning.items():
            meaning = merge_meanings(p_meaning, e_meaning)
            if True not in meaning or False not in meaning:
                continue
            quantifier = Quantifier(expression, presupposition)

            if meaning in quantifiers_by_meaning.keys():
                other_quantifier = quantifiers_by_meaning[meaning]

                this_complexity = setup.measure_quantifier_complexity(quantifier)
                other_complexity = setup.measure_quantifier_complexity(other_quantifier)
                if this_complexity >= other_complexity:
                    continue

            quantifiers_by_meaning[meaning] = quantifier

    return quantifiers_by_meaning