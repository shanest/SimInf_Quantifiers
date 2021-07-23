import argparse
from numpy import mean, float64
from pathos.multiprocessing import ProcessPool
from siminf import experiment_setups
from siminf import fileutil
from siminf import analysisutil
from siminf.fileutil import FileUtil

from siminf.languages import language_loader

def measure_monotonicity(language):
    from numpy import float64, mean
    mono_list = [float64(word.monotonicity) for word in language]
    mean_value = mean(mono_list)
    return mean_value


def main(args):
    setup = experiment_setups.parse(args.setup)
    dirname = fileutil.run_dir(setup.dest_dir, setup.name, setup.max_quantifier_length, setup.model_size, args.name)
    file_util = FileUtil(dirname)
    languages = language_loader.load_languages(file_util)
    
    with ProcessPool(nodes=setup.processes) as process_pool:
        monotonicities = process_pool.map(measure_monotonicity, languages)

    file_util.dump_dill(monotonicities, 'monotonicity.dill')

    print("measure_monotonicity.py finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze")
    #common arguments
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--name', required=True)
    #parse args
    args = parser.parse_args()
    main(args)