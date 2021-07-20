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
    
    file_util = FileUtil(fileutil.run_dir(setup.dest_dir, setup.name, setup.max_quantifier_length, setup.model_size, setup.natural_name))
    
    languages = language_loader.load_languages(file_util)
    
    universe = generator.generate_simplified_models(setup.model_size)
    
    pool = ProcessPool(nodes=setup.processes)
    
    if setup.inf_strat == 'exact':
        informativeness_measurer = InformativenessMeasurer(len(universe))
    elif setup.inf_strat == 'simmax':
        informativeness_measurer = SimMaxInformativenessMeasurer(universe)
    else:
        raise ValueError('{0} is not a valid informativeness strategy.'.format(args.inf_strat))
    
    if setup.comp_strat == 'wordcount':
        complexity_measurer = WordCountComplexityMeasurer(setup.max_words)
    elif setup.comp_strat == 'wordcomplexity':
        complexity_measurer = SumComplexityMeasurer(setup.max_words, 1)
    else:
        raise ValueError('{0} is not a valid complexity strategy.'.format(setup.comp_strat))
    
    informativeness = pool.map(informativeness_measurer, languages)
    complexity = pool.map(complexity_measurer, languages)
    
    file_util.dump_dill(informativeness, 'informativeness_{0}.dill'.format(setup.inf_strat))
    file_util.dump_dill(complexity, 'complexity_{0}.dill'.format(setup.comp_strat))
    
    print("measure.py finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure Languages")
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    args = parser.parse_args()
    
    main(args)