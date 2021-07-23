import argparse
from numpy import mean
from numpy import float64
from pathos.multiprocessing import ProcessPool

from siminf import fileutil
from siminf.fileutil import FileUtil 
from siminf import experiment_setups 
from siminf import analysisutil
from siminf.languages import language_loader

def measure_conservativity(language):
    from numpy import float64
    cons_list = [float64(word.conservativity) for word in language]
    return mean(cons_list)


def main(args):
    setup = experiment_setups.parse(args.setup)
    dirname = fileutil.run_dir(setup.dest_dir, setup.name, setup.max_quantifier_length, setup.model_size, args.name)
    file_util = FileUtil(dirname)
    
    languages = language_loader.load_languages(file_util)

    with ProcessPool(nodes=setup.processes) as process_pool:
        conservativities = process_pool.map(measure_conservativity, languages)

    file_util.dump_dill(conservativities, 'conservativity.dill')
    
    print("measure_conservativity.py finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze")
    #common arguments
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--name', required=True)
    #parse
    args = parser.parse_args()
    main(args)