import analysisutil
import matplotlib.pyplot as plt
import numpy as np
import plotnine as pn

analysisutil.add_argument('table_name')
analysisutil.add_argument('bins', type=int)

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

data = file_util.load_pandas_csv('pandas_{0}.csv'.format(args.table_name))

comm_cost = np.array(data['comm_cost'])
complexity = np.array(data['complexity'])
monotonicity = np.array(data['naturalness'])

fig = plt.figure()
plt.scatter(comm_cost, complexity)
plt.show()

max_comp = max(complexity)
min_comp = min(complexity)
max_inf = max(comm_cost)
min_inf = min(comm_cost)
comp_step = (max_comp-min_comp)/args.bins
inf_step = (max_inf-min_inf)/args.bins

plot_complexity = []
plot_informativeness = []
plot_avg_monotonicity = []

for comp_start in np.arange(min_comp,max_comp,comp_step):
    comp_end = comp_start+comp_step
    for inf_start in np.arange(min_inf,max_inf,inf_step):
        monotonicities = []
        inf_end = inf_start+inf_step
        for (i,(inf,comp,mono)) in enumerate(zip(comm_cost,complexity,monotonicity)):
            if comp_start < comp <= comp_end and inf_start < inf <= inf_end:
                monotonicities.append(mono)
        if len(monotonicities) > 0:
            plot_complexity.append(comp_start + comp_step/2)
            plot_informativeness.append(inf_start + inf_step/2)
            plot_avg_monotonicity.append(np.mean(monotonicities))

fig = plt.figure()
plt.scatter(plot_informativeness,plot_complexity,c=plot_avg_monotonicity, s=(235/args.bins)**2, marker='s')
plt.colorbar()

plt.xlabel('comm_cost')
plt.ylabel('complexity')

plt.show()

file_util.save_figure(fig, '{0}_{1}_plot_avg_monotonicity_{2}bins'.format(
    args.complexity_strategy,
    args.informativeness_strategy,
    args.bins
))
