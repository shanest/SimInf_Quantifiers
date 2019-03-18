import argparse
import os

import dill
from pathos.pools import ProcessPool

import ExperimentSetups
import Generator

# Parameters
parser = argparse.ArgumentParser(description="Generate Quantifiers")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('max_quantifier_length', type=int)
parser.add_argument('model_size', type=int)
parser.add_argument('--dest_dir', default='results')
parser.add_argument('--processes', default=4, type=int)
parser.add_argument('--skipexpressions', default=False, action="store_true")

args = parser.parse_args()

processes = args.processes
setup = ExperimentSetups.parse(args.setup)
max_quantifier_length = args.max_quantifier_length
model_size = args.model_size

universe = setup.generate_models(model_size)

folderName = "{0}/{1}_length={2}_size={3}".format(args.dest_dir,setup.name,max_quantifier_length,model_size)
os.makedirs("{0}".format(folderName), exist_ok=True)

if not args.skipexpressions:
    processpool = ProcessPool(nodes=processes)
    expression_generator = Generator.ExpressionGenerator(setup, model_size, universe, processpool)
    (generated_expressions_dict, expressions_by_meaning) = \
        expression_generator.generate_all_expressions(max_quantifier_length)
    with open('{0}/generated_expressions.dill'.format(folderName), 'wb') as file:
        dill.dump(expressions_by_meaning, file)

    processpool.close()
    processpool.join()
else:
    with open('{0}/generated_expressions.dill'.format(folderName), 'rb') as file:
        expressions_by_meaning = dill.load(file)

print("{0} expressions!".format(len(expressions_by_meaning[bool].values())))

quantifiers_by_meaning = Generator.add_presuppositions(setup, expressions_by_meaning[bool])

print("Quantifiers generated.")

generated_quantifiers = list(quantifiers_by_meaning.values())
generated_meanings = list(quantifiers_by_meaning.keys())

print("Quantifiers listed.")

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
