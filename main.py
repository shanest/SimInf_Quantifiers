import json
from Expression import *
from GeneralizedQuantifierModel import *
from itertools import chain,combinations

string_to_function = {
    "subset": lambda model, x, y: x <= y,
    ">": lambda model, x, y: x > y,
    "/": lambda model, x, y: x / y if y > 0 else 0,
    "-": lambda model, x, y: x - y,
    "card": lambda model, x: len(x),
    "intersection": lambda model, x, y: x & y,
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
        func = string_to_function[spec[0]]
        arg_expressions = []
        for arg_spec in spec[1:]:
            arg_expressions.append(parse_expression(arg_spec))
        return Expression(spec[0], func, *arg_expressions)

    if isinstance(spec, float):
        func = Primitives.create_num_func(spec)
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
