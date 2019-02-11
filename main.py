import json
from Expression import *
from GeneralizedQuantifierModel import *
from itertools import chain,combinations
import numpy as np
import random
import matplotlib.pyplot as plt
from Operator import operators,operatorsByReturnType
import json

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


def parse_expression(spec):
    if isinstance(spec, list):
        func = operators[spec[0]].func
        arg_expressions = []
        for arg_spec in spec[1:]:
            arg_expressions.append(parse_expression(arg_spec))
        return Expression(spec[0], func, *arg_expressions)

    if isinstance(spec, float) or isinstance(spec, int):
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


def generate_expression(return_type, size, max_integer):
    if size == 0:
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

    (name, operator) = random.choice(operatorsByReturnType[return_type])

    arg_expressions = []
    size_left = size-1
    for arg_type in operator.inputTypes:
        arg_size = random.choice(range(size_left)) if size_left > 0 else 0
        size_left -= arg_size
        arg_expressions.append(generate_expression(arg_type, arg_size, max_integer))

    return Expression(name, operator.func, *arg_expressions)


# Measure complexity of each quantifier
def calculate_complexity(expression):
    return expression.length()/10


# Measure communicative cost of each quantifier
def calculate_communicative_cost(expression, universe):
    true_count = 0
    for model in universe:
        if expression.evaluate(model):
            true_count += 1
    return true_count / len(universe) if true_count > 0 else 1


# Parameters
model_size = 7
designated_quantifier_lengths = [2,3,4,5,6,7,8]

# Initialize universe
universe = generate_models(model_size)

# Read lexicalized quantifiers from data file
with open('EnglishQuantifiers.json') as json_file:
    data = json.load(json_file)

quantifier_specs = data['quantifiers']
quantifier_expressions = parse_quantifiers(quantifier_specs)

# Generate quantifiers
generated_quantifier_expressions = []
for length in designated_quantifier_lengths:
    for i in range(50):
        generated_quantifier_expressions.append(generate_expression(bool, length, model_size))

# Measure cost and complexity for non-generated quantifiers
cost = {}
complexity = {}
for name, expression in quantifier_expressions.items():
    cost[name] = calculate_communicative_cost(expression,universe)
    complexity[name] = calculate_complexity(expression)
    plt.annotate(name,(cost[name],complexity[name]))

with open('./results/lexicalized_quantifiers_cost.txt', 'w') as f:
    for (name,value) in cost.items():
        f.write("{0}: {1}\n".format(name, value))

with open('./results/lexicalized_quantifiers_complexity.txt', 'w') as f:
    for (name,value) in complexity.items():
        f.write("{0}: {1}\n".format(name, value))


# Measure cost and complexity for generated quantifiers
generated_cost = []
generated_complexity = []
for expression in generated_quantifier_expressions:
    generated_cost.append(calculate_communicative_cost(expression,universe))
    generated_complexity.append(calculate_complexity(expression))

with open('./results/generated_quantifiers.txt', 'w') as f:
    for expression in generated_quantifier_expressions:
        f.write("{0}\n".format(expression.to_string()))

np.savetxt('./results/generated_quantifiers_cost.txt',generated_cost)
np.savetxt('./results/generated_quantifiers_complexity.txt',generated_complexity)

# Plot
plt.plot(generated_cost,generated_complexity,'o',color='grey')
plt.plot(cost.values(),complexity.values(),'o')

# for i in range(len(generated_quantifier_expressions)):
#     plt.annotate(str(i),(generated_cost[i],generated_complexity[i]))

plt.axis([0,1,0,1])
plt.show()