from numpy import mean
from numpy import float64
from pathos.multiprocessing import ProcessPool

import analysisutil
from Languages import LanguageLoader

(args, setup, file_util) = analysisutil.init()

languages = LanguageLoader.load_languages(file_util)


def measure_conservativity(language):
    return mean([float64(word.conservativity) for word in language])


with ProcessPool(nodes=args.processes) as process_pool:
    conservativities = process_pool.map(measure_conservativity, languages)

file_util.dump_dill(conservativities, 'conservativity.dill')