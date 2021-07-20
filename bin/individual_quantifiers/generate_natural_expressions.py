import json
import os

from siminf import analysisutil
from siminf import generator
from siminf import parser


def main():

    (args, setup, file_util) = analysisutil.init(use_base_dir=True)
    
    expressions = file_util.load_dill('expressions.dill')
    meanings = file_util.load_dill('meanings.dill')
    universe = generator.generate_simplified_models(setup.model_size)
    
    filename = os.path.join(os.path.dirname(args.setup),'natural_expressions/{0}.json'.format(setup.name))
    
    with open(filename, 'r') as file:
        specs = json.load(file)
    
    natural_expressions = []
    for spec in specs:
        natural_expressions.extend(parser.parse_expression_options(spec, setup.model_size))
    
    natural_meanings = map(generator.MeaningCalculator(universe), natural_expressions)
    
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
    print("generate_natural_expressions.py finished.")
    
if __name__ == "__main__":
    main()
