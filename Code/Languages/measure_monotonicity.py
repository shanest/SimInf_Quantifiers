from statistics import mean

from pathos.multiprocessing import ProcessPool

import analysisutil

(args, setup, file_util) = analysisutil.init()

languages = file_util.load_dill('languages.dill')


def measure_monotonicity(language):
    return mean([word.monotonicity for word in language])


with ProcessPool(nodes=args.processes) as process_pool:
    monotonicities = process_pool.map(measure_monotonicity, languages)

file_util.dump_dill(monotonicities, 'monotonicity.dill')