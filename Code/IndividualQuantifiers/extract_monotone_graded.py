from pathos.multiprocessing import ProcessPool

import Generator
import analysisutil
from Monotonicity import MonotonicityMeasurer

analysisutil.add_argument('threshold', type=float)

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

expressions = file_util.load_dill('expressions.dill')
raw_meanings = file_util.load_dill('meanings.dill')

universe = Generator.generate_simplified_models(args.model_size)


def get_monotone_quantifiers(monotone_set, threshold, process_pool):
    measurer = MonotonicityMeasurer(universe, args.model_size, monotone_set)
    monotonicities = process_pool.map(measurer, raw_meanings)
    return set(i for (i, monotonicity) in enumerate(monotonicities) if monotonicity > threshold)


with ProcessPool(nodes=args.processes) as process_pool:
    a = get_monotone_quantifiers('A', args.threshold, process_pool)
    b = get_monotone_quantifiers('B', args.threshold, process_pool)

indices = a.union(b)

file_util.dump_dill(indices, 'monotone_{0}_expression_indices.dill'.format(args.threshold))
