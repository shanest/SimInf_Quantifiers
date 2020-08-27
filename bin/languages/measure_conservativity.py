import argparse
from numpy import mean
from numpy import float64
from pathos.multiprocessing import ProcessPool

from siminf import fileutil
from siminf.fileutil import FileUtil 
from siminf import experiment_setups 
from siminf import analysisutil
from siminf.languages import language_loader

def measure_conservativity(languages):
    from numpy import float64
    float_list = [float64(word.conservativity) for word in languages]
    return mean([float64(word.conservativity) for word in languages])

def measure_conservativity(conservativity_list):
    from numpy import mean
    value = mean(conservativity_list)
    return value

def main(args):
    setup = experiment_setups.parse(args.setup)
    dirname = fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name)
    file_util = FileUtil(dirname)
    
    #languages = LanguageLoader.load_languages(file_util)
    languages = language_loader.load_all_evaluated_expressions(file_util)
    conservativity_list = [float64(word.conservativity) for word in languages]

    with ProcessPool(nodes=args.processes) as process_pool:
        # conservativities = process_pool.map(measure_conservativity, languages)
        conservativities = process_pool.map(measure_conservativity, conservativity_list)

    file_util.dump_dill(conservativities, 'conservativity.dill')
    
    print("measure_conservativity.py finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze")
    #common arguments
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--max_quantifier_length', type=int, required=True)
    parser.add_argument('--model_size', type=int, required=True)
    parser.add_argument('--dest_dir', default='results')
    parser.add_argument('--processes', default=4, type=int)
    parser.add_argument('--name', default='run_0')
    #parse
    args = parser.parse_args()
    main(args)