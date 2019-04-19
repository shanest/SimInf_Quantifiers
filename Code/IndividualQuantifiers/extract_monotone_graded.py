import analysisutil

analysisutil.add_argument('threshold', type=float)

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

threshold = round(args.threshold, 2)


def get_monotone_indices(monotone_set, direction, threshold):
    monotonicities = file_util.load_dill('monotonicities_{0}_{1}'.format(monotone_set, direction))
    return set(i for (i, monotonicity) in enumerate(monotonicities) if monotonicity > threshold)


indices_upward = get_monotone_indices('b', 'up', threshold)
indices_downward = get_monotone_indices('b', 'down', threshold)

indices = indices_upward.union(indices_downward)

file_util.dump_dill(indices, 'monotone_{0}_expression_indices.dill'.format(threshold))
