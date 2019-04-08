import argparse

import ExperimentSetups
import fileutil
from fileutil import FileUtil

parser = argparse.ArgumentParser(description="Analyze")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('max_quantifier_length', type=int)
parser.add_argument('model_size', type=int)
parser.add_argument('--dest_dir', default='results')
parser.add_argument('--processes', default=4, type=int)
parser.add_argument('--name', default='run_0')

add_argument = parser.add_argument


def init():
    args = parser.parse_args()
    setup = ExperimentSetups.parse(args.setup)
    file_util = FileUtil(fileutil.run_dir(
        args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name))
    return args, setup, file_util