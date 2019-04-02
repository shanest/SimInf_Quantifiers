import argparse
from pathos.pools import ProcessPool

import ExperimentSetups

# Parameters
from fileutil import FileUtil

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

file_util = FileUtil(args.dest_dir, setup.name, max_quantifier_length, model_size)

folderName = "{0}/{1}_length={2}_size={3}".format(args.dest_dir,setup.name,max_quantifier_length,model_size)

processpool = ProcessPool(nodes=processes)

expressions = file_util.load_dill('expressions.dill')

complexities = processpool.map(setup.measure_expression_complexity, expressions)

file_util.dump_dill(complexities, 'expression_complexities.dill')

processpool.close()
processpool.join()

print('Complexity Measuring finished.')
