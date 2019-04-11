import argparse
import json

import ExperimentSetups
import Generator
import Parser
import fileutil
from Languages.ComplexityMeasurer import WordCountComplexityMeasurer, SumComplexityMeasurer
from Languages.InformativenessMeasurer import SimMaxInformativenessMeasurer, InformativenessMeasurer
from Languages.LanguageGenerator import EvaluatedExpression
from fileutil import FileUtil
import os

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
parser.add_argument('--name', default='run_0')

args = parser.parse_args()

setup = ExperimentSetups.parse(args.setup)

file_util = FileUtil(fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name))

universe = Generator.generate_simplified_models(args.model_size)

if args.inf_strat == 'exact':
    informativeness_measurer = InformativenessMeasurer(len(universe))
elif args.inf_strat == 'simmax':
    informativeness_measurer = SimMaxInformativenessMeasurer(universe)
else:
    raise ValueError('{0} is not a valid informativeness strategy.'.format(args.inf_strat))

if args.comp_strat == 'wordcount':
    complexity_measurer = WordCountComplexityMeasurer(args.max_words)
elif args.comp_strat == 'wordcomplexity':
    complexity_measurer = SumComplexityMeasurer(args.max_words, 1)
else:
    raise ValueError('{0} is not a valid complexity strategy.'.format(args.comp_strat))

languages_dir = setup.natural_languages_dirname

languages = []
language_names = []

calculate_meaning = Generator.MeaningCalculator(universe)


def parse_language(filename):
    with open(filename, 'r') as file:
        spec_dict = json.load(file)
    language = []
    for spec in spec_dict.values():
        expression = Parser.parse_expression(spec,setup)
        complexity = setup.measure_expression_complexity(expression, args.max_quantifier_length)
        meaning = calculate_meaning(expression)
        language.append(EvaluatedExpression(expression, meaning, complexity))
    return language


for filename in os.listdir(languages_dir):
    if filename.endswith('.json'):
        languages.append(parse_language(os.path.join(languages_dir, filename)))
        language_names.append(filename[:-5])  # Name without extension

informativeness = zip(language_names, map(informativeness_measurer, languages))
complexity = zip(language_names, map(complexity_measurer, languages))

file_util.dump_dill(informativeness, 'informativeness_{0}_{1}.dill'.format(setup.name, args.inf_strat))
file_util.dump_dill(complexity, 'complexity_{0}_{1}.dill'.format(setup.name, args.comp_strat))

