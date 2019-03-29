import argparse

import ExperimentSetups
from fileutil import FileUtil

parser = argparse.ArgumentParser(description="Analyze")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('max_quantifier_length', type=int)
parser.add_argument('model_size', type=int)
parser.add_argument('--dest_dir', default='results')
parser.add_argument('--processes', default=4, type=int)

args = parser.parse_args()
setup = ExperimentSetups.parse(args.setup)

file_util = FileUtil(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size)