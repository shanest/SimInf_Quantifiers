import argparse
import json

from siminf import experiment_setups
from siminf import generator
from siminf import parser as siminf_parser
from siminf import fileutil
from siminf.languages.complexity_measurer import WordCountComplexityMeasurer, SumComplexityMeasurer
from siminf.languages.informativeness_measurer import SimMaxInformativenessMeasurer, InformativenessMeasurer
from siminf.languages.language_generator import EvaluatedExpression
from siminf.fileutil import FileUtil
import os

def parse_language(filename, setup, universe):
    calculate_meaning = generator.MeaningCalculator(universe)
    with open(filename, 'r') as file:
        spec_dict = json.load(file)
    language = []
    for spec in spec_dict.values():
        expression = siminf_parser.parse_expression(spec, setup)
        complexity = setup.measure_expression_complexity(expression, args.max_quantifier_length)
        meaning = calculate_meaning(expression)
        
        # TO DO: the following 4 measurement must be calculated
        #monotonicity
        monotonicity = 0.5
        
        #conservativity
        conservativity = 0.5
        
        #special_complexity
        special_complexity = 0.5
        
        #index
        index = 0
        
        #language.append(EvaluatedExpression(expression, meaning, complexity))
        language.append(EvaluatedExpression(expression, meaning, complexity, monotonicity, \
                                            conservativity, special_complexity, index))
    return language

def main(args):
    setup = experiment_setups.parse(args.setup)
    
    file_util = FileUtil(fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name))
    
    universe = generator.generate_simplified_models(args.model_size)

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

    for filename in os.listdir(languages_dir):
        if filename.endswith('.json'):
            language_file = os.path.join(languages_dir, filename)
            language = parse_language(language_file, setup, universe)
            languages.append(language)
            language_names.append(filename[:-5])  # Name without extension

    informativeness = zip(language_names, map(informativeness_measurer, languages))
    complexity = zip(language_names, map(complexity_measurer, languages))

    file_util.dump_dill(informativeness, 'informativeness_{0}_{1}.dill'.format(setup.name, args.inf_strat))
    file_util.dump_dill(complexity, 'complexity_{0}_{1}.dill'.format(setup.name, args.comp_strat))

    print("measure_lexicalized.py finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure Languages")
    #common arguments
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--max_quantifier_length', type=int, required=True)
    parser.add_argument('--model_size', type=int, required=True)
    parser.add_argument('--dest_dir', default='results')
    parser.add_argument('--processes', default=4, type=int)
    parser.add_argument('--name', default='run_0')
    #additional arguments
    parser.add_argument('--max_words', type=int, required=True)
    parser.add_argument('--comp_strat', required=True)
    parser.add_argument('--inf_strat', required=True)
    parser.add_argument('--sample', type=int, default=None)
    
    args = parser.parse_args()
    main(args)
