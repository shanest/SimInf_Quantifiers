import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('complexity_strategy')
analysisutil.add_argument('informativeness_strategy')

(args, setup, file_util) = analysisutil.init()

informativeness = file_util.load_dill('informativeness_{0}.dill'.format(args.informativeness_strategy))
complexity = file_util.load_dill('complexity_{0}.dill'.format(args.complexity_strategy))
monotonicity = file_util.load_dill('monotonicity.dill')

inf_weight = .5*max(informativeness)
comp_weight = .5*max(complexity)

combined = [inf*inf_weight + comp*comp_weight for (inf, comp) in zip(informativeness, complexity)]

fig = plt.figure()
plt.scatter(monotonicity, combined)

plt.ylabel('combined')
plt.xlabel('monotonicity')

plt.show()

file_util.save_figure(fig, '{0}_{1}_plot_monotonicity_combined'.format(
    args.complexity_strategy,
    args.informativeness_strategy
))
