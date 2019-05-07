import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('-i','--indices', nargs='*')
(args, setup, file_util) = analysisutil.init(use_base_dir=True)

monotonicities = file_util.load_dill('monotonicities_max.dill')

if args.indices is not None:
    index_sets = []
    for indices_name in args.indices:
        index_sets.append(set(file_util.load_dill('{0}_expression_indices.dill'.format(indices_name))))
    indices = set.intersection(*index_sets)
    monotonicities = [monotonicities[i] for i in indices]

fig = plt.figure()

plt.hist(monotonicities, bins=30)

plt.show()
file_util.save_figure(fig, 'monotonicity_hist{0}'.format('_{0}'.format(args.indices) if args.indices is not None else ''))
