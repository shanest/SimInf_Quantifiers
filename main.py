import json
from Expression import *
from GeneralizedQuantifierModel import *
from itertools import chain,combinations

string_to__expression_type = {
    "A": PrimitiveExpression,
    "B": PrimitiveExpression,
    "M": PrimitiveExpression,
    "subset": SubsetExpression
}

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

model_size = 7
M = set(range(model_size))

M_powerset = list(powerset(M))

models = []

for A in M_powerset:
    for B in M_powerset:
        models.append(GeneralizedQuantifierModel(M, set(A), set(B)))

def parse_expression(spec):
    if isinstance(spec[0],str):
        expression_type = string_to__expression_type[spec[0]]
    else
        expression_type = NumberExpression

    if len(spec) == 1:
        return expression_type(spec[0])
    if len(spec) == 2:
        arg1 = parse_expression(spec[1])
        return expression_type(arg1)
    if len(spec) == 3:
        arg1 = parse_expression(spec[1])
        arg2 = parse_expression(spec[2])
        return expression_type(arg1, arg2)


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
informativeness = {}
for name, expression in quantifier_expressions.items():
    true_count = 0
    for model in models:
        if expression.evaluate(model):
            true_count += 1

informativeness[name] = true_count / len(models)

# Plot
print(complexity)
print(informativeness)
