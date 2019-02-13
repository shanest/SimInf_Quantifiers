from GeneralizedQuantifierModel import *
from itertools import chain,combinations
from Expression import *
import random
import numpy as np
from Operator import operatorsByReturnType
import Generator
import Measurer


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


def generate_primitive_expression(return_type, max_integer):
    if return_type == int:
        x = random.choice(range(max_integer))
        return Expression(x, Primitives.create_value_func(x))
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


def generate_unique_expressions(lengths, amount_per_length, max_integer, universe):
    generated_quantifier_by_meaning = {}
    for length in lengths:
        print("Start generating length {0}".format(length))
        for i in range(amount_per_length):
            new_better_expression = False
            while not new_better_expression:
                expression = Generator.generate_expression(bool, length, max_integer)
                meaning = tuple([expression.evaluate(model) for model in universe])

                if meaning in generated_quantifier_by_meaning.keys():
                    other_expression = generated_quantifier_by_meaning[meaning]

                    this_complexity = Measurer.measure_complexity(expression)
                    other_complexity = Measurer.measure_complexity(other_expression)
                    if this_complexity > other_complexity:
                        continue

                generated_quantifier_by_meaning[meaning] = expression
                new_better_expression = True

    return list(generated_quantifier_by_meaning.values())
