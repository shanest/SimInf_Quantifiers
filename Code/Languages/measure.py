import argparse
from pathos.pools import ProcessPool

import ExperimentSetups
import Generator
from Languages.ComplexityMeasurer import WordCountComplexityMeasurer, SumComplexityMeasurer
from Languages.InformativenessMeasurer import SimMaxInformativenessMeasurer, InformativenessMeasurer
from fileutil import FileUtil

parser = argparse.ArgumentParser(description="Measure Languages")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('max_quantifier_length', type=int)
parser.add_argument('model_size', type=int)
parser.add_argument('max_words', type=int)
parser.add_argument('comp_strat')
parser.add_argument('inf_strat')
parser.add_argument('--sample', type=int, default=None)
parser.add_argument('--dest_dir', default='results')
parser.add_argument('--processes', default=4, type=int)

args = parser.parse_args()

setup = ExperimentSetups.parse(args.setup)

file_util = FileUtil(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size)

languages = file_util.load_dill('languages.dill')

universe = Generator.generate_simplified_models(args.model_size)

pool = ProcessPool(nodes=args.processes)

if args.inf_strat == 'exact':
    informativeness_measurer = InformativenessMeasurer(len(universe))
elif args.inf_strat == 'simmax':
    informativeness_measurer = SimMaxInformativenessMeasurer(universe)
else:
    raise ValueError('{0} is not a valid informativeness strategy.'.format(args.inf_strat))

if args.comp_strat == 'wordcount':
    complexity_measurer = WordCountComplexityMeasurer(args.max_words)
elif args.comp_strat == 'wordcomplexity':
    complexity_measurer = SumComplexityMeasurer(args.max_words, args.max_quantifier_length/20)
else:
    raise ValueError('{0} is not a valid complexity strategy.'.format(args.inf_strat))


informativeness = pool.map(informativeness_measurer, languages)
complexity = pool.map(complexity_measurer, languages)


file_util.dump_dill(informativeness, 'informativeness_{0}.dill'.format(args.inf_strat))
file_util.dump_dill(complexity, 'complexity_{0}.dill'.format(args.comp_strat))

