import argparse
import random
from collections import namedtuple
from pathos.multiprocessing import ProcessPool

from siminf import generator
from siminf import analysisutil
from siminf import fileutil 
from siminf.fileutil import FileUtil 
from siminf import experiment_setups 
from siminf.languages.complexity_measurer import WordCountComplexityMeasurer
from siminf.languages.informativeness_measurer import InformativenessMeasurer, SimMaxInformativenessMeasurer
from siminf.languages.language_generator import generate_all, generate_sampled, EvaluatedExpression

def main(args):   
    setup = experiment_setups.parse(args.setup)
    dirname = fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name)
    file_util = FileUtil(dirname)
    
    languages = []
    universe = generator.generate_simplified_models(args.model_size)

    FakeEvaluatedExpression = namedtuple('FakeEvaluatedExpression', 'meaning')
    expressions = [FakeEvaluatedExpression(tuple([random.choice([True, False]) for model in universe]))
                    for i in range(args.random_size)]

    if args.sample is None:
        print("generate_all() called.")
        languages = generate_all(expressions, args.max_words, args.fixedwordcount)
    else:
        print("generate_sampled() called.")
        languages = generate_sampled(expressions, args.max_words, args.sample)

    complexity_measurer = WordCountComplexityMeasurer(args.max_words)
    informativeness_measurer_exact = InformativenessMeasurer(len(universe))
    informativeness_measurer_simmax = SimMaxInformativenessMeasurer(universe)

    with ProcessPool(nodes=args.processes) as pool:
        complexity = pool.map(complexity_measurer, languages)
        informativeness_exact = pool.map(informativeness_measurer_exact, languages)
        informativeness_simmax = pool.map(informativeness_measurer_simmax, languages)

    file_util.dump_dill(complexity, 'complexity_wordcount.dill')
    file_util.dump_dill(informativeness_exact, 'informativeness_exact.dill')
    file_util.dump_dill(informativeness_simmax, 'informativeness_simmax.dill')
    
    print("coinflip_languages.py finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze")
    #common arguments
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--max_quantifier_length', type=int, required=True)
    parser.add_argument('--model_size', type=int, required=True)
    parser.add_argument('--dest_dir', default='results')
    parser.add_argument('--processes', default=4, type=int)
    parser.add_argument('--name', default='run_0')
    #additional arguments
    parser.add_argument('--max_words', type=int, required=True)
    parser.add_argument('--fixedwordcount', type=int)
    parser.add_argument('--sample', type=int)
    parser.add_argument('--random_size', type=int, default=100)
    #parse
    args = parser.parse_args()
    main(args)

