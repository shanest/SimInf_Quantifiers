import argparse
import json
import os
import sys

import dill

import ExperimentSetups
import Generator
import debug

# Parameters
parser = argparse.ArgumentParser(description="Generate Quantifiers")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('max_quantifier_length', type=int)
parser.add_argument('model_size', type=int)
parser.add_argument('--dest_dir', default='results')
parser.add_argument('--processes', default=4, type=int)

args = parser.parse_args()

processes = args.processes
setup = ExperimentSetups.parse(args.setup)
max_quantifier_length = args.max_quantifier_length
model_size = args.model_size

universe = setup.generate_models(model_size)

(generated_expressions_dict, expressions_by_meaning) = \
    Generator.generate_all_expressions(
        setup,
        max_quantifier_length,
        model_size,
        universe,
        processes
    )

print("{0} expressions!".format(len(expressions_by_meaning[bool].values())))

quantifiers_by_meaning = Generator.add_presuppositions(setup, expressions_by_meaning[bool])

print("Quantifiers generated.")

generated_quantifiers = list(quantifiers_by_meaning.values())
generated_meanings = list(quantifiers_by_meaning.keys())

print("Quantifiers listed.")

folderName = "{0}/{1}_length={2}_size={3}".format(args.dest_dir,setup.name,max_quantifier_length,model_size)

print("Folder name formatted.")

os.makedirs("{0}".format(folderName), exist_ok=True)

print("Saving files....")

with open('{0}/generated_meanings.dill'.format(folderName), 'wb') as file:
    dill.dump(generated_meanings, file)

print("File 1 saved")

with open('{0}/generated_quantifiers.dill'.format(folderName), 'wb') as file:
    dill.dump(generated_quantifiers, file)

print("File 2 saved")

with open('{0}/generated_quantifiers.txt'.format(folderName), 'w') as f:
    for quantifier in generated_quantifiers:
        f.write("{0}\n".format(quantifier))

print('Generation finished')
