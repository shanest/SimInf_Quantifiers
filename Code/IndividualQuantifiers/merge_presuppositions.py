import argparse

import dill
from pathos.pools import ProcessPool

import Generator, ExperimentSetups

parser = argparse.ArgumentParser(description="Generate Quantifiers")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('max_quantifier_length', type=int)
parser.add_argument('model_size', type=int)
parser.add_argument('--chunk_size', default=4, type=int)
parser.add_argument('--dest_dir', default='results')
parser.add_argument('--processes', default=4, type=int)

args = parser.parse_args()

processes = args.processes
chunk_size = args.chunk_size
setup = ExperimentSetups.parse(args.setup)
max_quantifier_length = args.max_quantifier_length
model_size = args.model_size

folderName = "{0}/{1}_length={2}_size={3}".format(args.dest_dir,setup.name,max_quantifier_length,model_size)

with open('{0}/generated_expressions.dill'.format(folderName), 'rb') as file:
    expressions_by_meaning = dill.load(file)

processpool = ProcessPool(nodes=processes)
merger = Generator.PresuppositionMerger(setup, processpool, chunk_size)

quantifiers_by_meaning = merger.add_presuppositions(expressions_by_meaning)

processpool.close()
processpool.join()

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