import argparse
from pathos.pools import ProcessPool
from siminf import experiment_setups
from siminf import generator
from siminf import fileutil
from siminf.languages import language_loader
from siminf.languages.complexity_measurer import WordCountComplexityMeasurer, SumComplexityMeasurer
from siminf.languages.informativeness_measurer import SimMaxInformativenessMeasurer, InformativenessMeasurer
from siminf.fileutil import FileUtil

def main(args):
    setup = experiment_setups.parse(args.setup)
    
    file_util = FileUtil(fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name))
    
    languages = language_loader.load_languages(file_util)
    
    universe = generator.generate_simplified_models(args.model_size)
    
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
        complexity_measurer = SumComplexityMeasurer(args.max_words, 1)
    else:
        raise ValueError('{0} is not a valid complexity strategy.'.format(args.comp_strat))
    
    informativeness = pool.map(informativeness_measurer, languages)
    complexity = pool.map(complexity_measurer, languages)
    
    file_util.dump_dill(informativeness, 'informativeness_{0}.dill'.format(args.inf_strat))
    file_util.dump_dill(complexity, 'complexity_{0}.dill'.format(args.comp_strat))
    
    print("measure.py finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure Languages")
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--max_quantifier_length', type=int, required=True)
    parser.add_argument('--model_size', type=int, required=True)
    parser.add_argument('--max_words', type=int, required=True)
    parser.add_argument('--comp_strat', required=True)
    parser.add_argument('--inf_strat', required=True)
    parser.add_argument('--sample', type=int, default=None)
    parser.add_argument('--dest_dir', default='results')
    parser.add_argument('--processes', default=4, type=int)
    parser.add_argument('--name', default='run_0')
    
    args = parser.parse_args()
    
    main(args)