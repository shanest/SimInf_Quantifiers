import json
from Expression import *
from GeneralizedQuantifierModel import *
from itertools import chain,combinations
from collections import namedtuple
import numpy as np
import random


Operator = namedtuple("Operator", "func inputTypes outputType")

operators = {
    "subset": Operator(
        lambda model, x, y: x <= y,
        [set,set],
        bool
    ),
    ">": Operator(
        lambda model, x, y: x > y,
        [float,float],
        bool
    ),
    "/": Operator(
        lambda model, x, y: x / y if y > 0 else 0,
        [int,int],
        float
    ),
    "diff": Operator(
        lambda model, x, y: x - y,
        [set,set],
        set
    ),
    "card": Operator(
        lambda model, x: len(x),
        [set],
        int
    ),
    "intersection": Operator(
        lambda model, x, y: x & y,
        [set,set],
        set
    )
}


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


model_size = 4
M = set(range(model_size))

M_powerset = list(powerset(M))

models = []

for A in M_powerset:
    for B in M_powerset:
        models.append(GeneralizedQuantifierModel(M, set(A), set(B)))


def parse_expression(spec):
    if isinstance(spec, list):
        func = operators[spec[0]].func
        arg_expressions = []
        for arg_spec in spec[1:]:
            arg_expressions.append(parse_expression(arg_spec))
        return Expression(spec[0], func, *arg_expressions)

    if isinstance(spec, float):
        func = Primitives.create_value_func(spec)
        return Expression(spec, func)

    if isinstance(spec, str):
        func = Primitives.create_set_func(spec)
        return Expression(spec, func)

    raise ValueError('Unexpected input format. Should be integer, string or list.')


def parse_quantifiers(specs):
    quantifier_expressions = {}
    for (name, spec) in specs.items():
        quantifier_expressions[name] = parse_expression(spec)
    return quantifier_expressions


# Read lexicalized quantifiers from data file
with open('EnglishQuantifiers.json') as json_file:
    data = json.load(json_file)

quantifier_specs = data['quantifiers']
quantifier_expressions = parse_quantifiers(quantifier_specs)

# Generate quantifiers
operatorsByReturnType = {
    set: [],
    bool: [],
    float: [],
    int: []
}
for (name, operator) in operators.items():
    operatorsByReturnType[operator.outputType].append((name,operator))

# for q in np.arange(0, 1, .1):
#     operatorsByReturnType[float].append(Operator(
#         Primitives.create_num_func(q),
#         [],
#         float
#     ))
#
# for set_name in ['A', 'B']:
#     operatorsByReturnType[set].append(Operator(
#         Primitives.create_set_func(set_name),
#         [],
#         set
#     ))


def generate_expression(return_type, size):
    if size == 0:
        if return_type == int:
            x = random.choice(range(model_size))
            return Expression(x,Primitives.create_value_func(x))
        if return_type == float:
            q = random.choice(np.arange(0, 1, .1))
            return Expression(q,Primitives.create_value_func(q))
        if return_type == set:
            set_name = random.choice(['A','B'])
            return Expression(set_name,Primitives.create_set_func(set_name))
        if return_type == bool:
            boolean = random.choice([True,False])
            return Expression(boolean,Primitives.create_value_func(boolean))

    (name, operator) = random.choice(operatorsByReturnType[return_type])

    arg_expressions = []
    size_left = size-1
    for arg_type in operator.inputTypes:
        arg_size = random.choice(range(size_left)) if size_left > 0 else 0
        size_left -= arg_size
        arg_expressions.append(generate_expression(arg_type, arg_size))

    return Expression(name, operator.func, *arg_expressions)

for i in range(100):
    quantifier_expressions[str(i)] = generate_expression(bool,5)
    print(quantifier_expressions[str(i)].to_string())

# Measure complexity of each quantifier
complexity = {}
for name, expression in quantifier_expressions.items():
    complexity[name] = expression.length()

# Measure communicative cost of each quantifier
cost = {}
for name, expression in quantifier_expressions.items():
    true_count = 0
    for model in models:
        if expression.evaluate(model):
            true_count += 1
    cost[name] = true_count / len(models)



# Plot
print(complexity)
print(cost)
