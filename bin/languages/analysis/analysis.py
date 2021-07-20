from pathos.multiprocessing import ProcessPool
import pandas as pd
import numpy as np
from numpy.linalg import norm
import pygmo
import plotnine as pn
from siminf import analysisutil

(args, setup, file_util) = analysisutil.init(use_base_dir=False)

# pareto_data = LanguageLoader.load_pandas_table(file_util.get_sub_file_util(args.pareto), 'wordcomplexity', 'simmax', include_monotonicity=False)

def load_data(file_util, complexity_strategy, informativeness_strategy):
    complexity = file_util.load_dill('complexity_{0}.dill'.format(complexity_strategy))
    informativeness = file_util.load_dill('informativeness_{0}.dill'.format(informativeness_strategy))

    data = {'complexity': complexity,
            'comm_cost': list(map(lambda x: 1 - x, informativeness))
           }
    for property in ('naturalness', 'monotonicity', 'conservativity'):
        fname = '{}.dill'.format(property)
        if file_util.exists(fname):
            data[property] = file_util.load_dill(fname)
    print(data)
    for key in data:
        print(key)
        print(len(data[key]))
    return pd.DataFrame(data)

main_data = load_data(file_util, args.comp_strat, args.inf_strat)
print(main_data)

base_plot = (pn.ggplot(pn.aes(x='comm_cost',y='complexity')) +
         pn.geom_point(pn.aes(color='factor(run)'), data=run_df))

print(base_plot)

plot = base_plot + pn.geom_point(data=pareto_data)
print(plot)


complexity = list(pareto_data['complexity'].values) + list(run_df['complexity'].values)
comm_cost = list(pareto_data['comm_cost'].values) + list(run_df['comm_cost'].values)


class MinEuclidianDistanceCalculator(object):

    def __init__(self, pareto_front):
        self.pareto_front = pareto_front

    def __call__(self, point):
        min_dist = np.Infinity
        for pareto_point in self.pareto_front:
            dist = norm(pareto_point-point)
            if dist < min_dist:
                min_dist = dist
        return min_dist


dominating_indices = pygmo.non_dominated_front_2d(list(zip(complexity,comm_cost)))
dominating_complexity = [complexity[i] for i in dominating_indices]
dominating_comm_cost = [comm_cost[i] for i in dominating_indices]
values = list(zip(dominating_comm_cost, dominating_complexity))

values.sort(key=lambda val: -val[1])
values.sort(key=lambda val: val[0])
values = [np.array(value) for value in values]

pareto_values = pd.DataFrame({'comm_cost': dominating_comm_cost, 'complexity': dominating_complexity})
plot = base_plot + pn.geom_point(data=pareto_values)
print(plot)

x = []
y = []
interval = .001

for (left, right) in zip(values[:-1], values[1:]):
    diff = right - left
    if norm(diff) == 0:
        continue
    amount_in_between = int(np.floor(norm(diff) / interval))
    normalized_diff = diff / norm(diff)
    for i in range(1,amount_in_between+1):
        point = left + i*interval*normalized_diff
        x.append(point[0])
        y.append(point[1])
    x.append(left[0])
    y.append(left[1])
    x.append(right[0])
    y.append(right[1])

estimated_pareto = pd.DataFrame({'comm_cost':x, 'complexity':y})


plot = base_plot + pn.geom_point(data=estimated_pareto)
print(plot)

dist_calculator = MinEuclidianDistanceCalculator(np.array(list(zip(x,y))))


with ProcessPool(nodes=args.processes) as pool:
    comm_cost = list(run_df['comm_cost'].values)
    complexity = list(run_df['complexity'].values)
    points = np.array(list(zip(comm_cost, complexity)))
    distances = pool.map(dist_calculator, points)
    run_df['pareto_closeness'] = distances

file_util.save_pandas_csv(run_df, 'pandas_{0}.csv'.format(args.table_name))