import analysisutil
import matplotlib.pyplot as plt
import numpy as np

analysisutil.add_argument('complexity_strategy')
analysisutil.add_argument('informativeness_strategy')
analysisutil.add_argument('bins', type=int)

(args, setup, file_util) = analysisutil.init()

informativeness = file_util.load_dill('informativeness_{0}.dill'.format(args.informativeness_strategy))
complexity = file_util.load_dill('complexity_{0}.dill'.format(args.complexity_strategy))
monotonicity = file_util.load_dill('monotonicity.dill')

max_comp = max(complexity)
max_inf = max(informativeness)
comp_step = max_comp/args.bins
inf_step = max_inf/args.bins

plot_complexity = []
plot_informativeness = []
plot_avg_monotonicity = []

for comp_start in np.arange(0,max_comp,comp_step):
    comp_end = comp_start+comp_step
    for inf_start in np.arange(0,max_inf,inf_step):
        monotonicities = []
        inf_end = inf_start+inf_step
        for (i,(inf,comp,mono)) in enumerate(zip(informativeness,complexity,monotonicity)):
            if comp_start < comp <= comp_end and inf_start < inf <= inf_end:
                monotonicities.append(mono)
        if len(monotonicities) > 0:
            plot_complexity.append(comp_start + comp_step/2)
            plot_informativeness.append(inf_start + inf_step/2)
            plot_avg_monotonicity.append(np.mean(monotonicities))

fig = plt.figure()
plt.scatter(plot_informativeness,plot_complexity,c=plot_avg_monotonicity, s=(235/args.bins)**2, marker='s')
plt.colorbar()

plt.xlabel('informativeness')
plt.ylabel('complexity')

plt.show()

file_util.save_figure(fig, '{0}_{1}_plot_avg_monotonicity_{2}bins'.format(
    args.complexity_strategy,
    args.informativeness_strategy,
    args.bins
))
