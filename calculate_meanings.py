import argparse
import os
import dill

import ExperimentSetups
import Parser
from Generator import MeaningCalculator

parser = argparse.ArgumentParser(description="Calculate the meanings of the lexicalized quantifiers")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('model_size', type=int)
parser.add_argument('--dest_dir', default='results')

args = parser.parse_args()
setup = ExperimentSetups.parse(args.setup)

universe = setup.generate_models(args.model_size)

quantifiers = Parser.load_from_file(setup.lexical_quantifiers_filename, setup)

calculate_meaning = MeaningCalculator(universe)

meanings = {name: calculate_meaning(quantifier) for (name,quantifier) in quantifiers.items()}

os.makedirs('{0}/lexicalized_meanings'.format(args.dest_dir), exist_ok=True)
with open('{0}/lexicalized_meanings/{1}_size={2}.dill'.format(args.dest_dir,setup.name,args.model_size), 'wb') as file:
    dill.dump(meanings, file)
