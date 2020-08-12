import argparse
from pathos.pools import ProcessPool
# import analysisutil
from siminf import analysisutil
from siminf import experiment_setups
from siminf import fileutil
from siminf.fileutil import FileUtil
# from Languages import LanguageLoader
from siminf.languages import language_loader
# from Languages.ComplexityMeasurer import WordCountComplexityMeasurer, SumComplexityMeasurer, SpecialComplexityMeasurer
from siminf.languages.complexity_measurer import WordCountComplexityMeasurer, SumComplexityMeasurer, SpecialComplexityMeasurer

# analysisutil.add_argument('max_words', type=int)
# analysisutil.add_argument('comp_strat')
# (args, setup, file_util) = analysisutil.init()



def main(args):
    setup = experiment_setups.parse(args.setup)
    dirname = fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name)
    file_util = FileUtil(dirname)
    
    languages = language_loader.load_languages(file_util)
    if args.comp_strat == 'wordcount':
        complexity_measurer = WordCountComplexityMeasurer(args.max_words)
    elif args.comp_strat == 'wordcomplexity':
        complexity_measurer = SumComplexityMeasurer(args.max_words, 1)
    elif args.comp_strat == 'special':
        complexity_measurer = SpecialComplexityMeasurer(args.max_words)
    else:
        raise ValueError('{0} is not a valid complexity strategy.'.format(args.comp_strat))

    with ProcessPool(nodes=args.processes) as pool:
        complexity = pool.map(complexity_measurer, languages)

    file_util.dump_dill(complexity, 'complexity_{0}.dill'.format(args.comp_strat))
    
    print("measure_complexity.py finished.")

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
    parser.add_argument('--comp_strat', required=True)
    #parse
    args = parser.parse_args()
    main(args)

