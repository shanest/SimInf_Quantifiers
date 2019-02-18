from collections import namedtuple

from GeneralizedQuantifierModel import *
from itertools import chain, combinations, product
from Expression import *
import random
import numpy as np
from Operator import operatorsByReturnType
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
