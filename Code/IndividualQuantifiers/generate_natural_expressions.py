import json
import os

import Generator
import Parser
import analysisutil

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

expressions = file_util.load_dill('expressions.dill')
meanings = file_util.load_dill('meanings.dill')
universe = Generator.generate_simplified_models(args.model_size)

filename = os.path.join(os.path.dirname(args.setup),'NaturalExpressions/{0}.json'.format(setup.name))

with open(filename, 'r') as file:
    specs = json.load(file)

natural_expressions = []
for spec in specs:
    natural_expressions.extend(Parser.parse_expression_options(spec, args.model_size))

natural_meanings = map(Generator.MeaningCalculator(universe), natural_expressions)

natural_expression_indices = []

for (i,natural_meaning) in enumerate(natural_meanings):
    try:
        existing_index = next(i for (i, meaning) in enumerate(meanings) if meaning == natural_meaning)
        natural_expression_indices.append(existing_index)
    except StopIteration:
        print('No existing quantifier equivalent to {0} found'.format(natural_expressions[i]))
        pass

print([str(expressions[i]) for i in natural_expression_indices])
file_util.dump_dill(natural_expression_indices, 'natural_expression_indices.dill')