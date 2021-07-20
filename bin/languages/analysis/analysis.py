from pathos.multiprocessing import ProcessPool
import pandas as pd
import numpy as np
from numpy.linalg import norm
import pygmo
import plotnine as pn
from siminf import analysisutil
import statsmodels.formula.api as smf

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

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
    return pd.DataFrame(data)


main_data = load_data(file_util.get_sub_file_util(setup.natural_name), setup.comp_strat, setup.inf_strat)

pareto_data = load_data(file_util.get_sub_file_util(setup.pareto_name), setup.comp_strat, setup.inf_strat)


# combine complexities and costs
complexity = list(pareto_data['complexity'].values) + list(main_data['complexity'].values)
comm_cost = list(pareto_data['comm_cost'].values) + list(main_data['comm_cost'].values)


def calculate_min_distance(pareto_front, point):
    min_dist = np.Infinity
    for pareto_point in pareto_front:
        dist = norm(pareto_point-point)
        if dist < min_dist:
            min_dist = dist
    return min_dist


# estimate pareto frontier
# TODO: clean this up!!
dominating_indices = pygmo.non_dominated_front_2d(list(zip(complexity,comm_cost)))
dominating_complexity = [complexity[i] for i in dominating_indices]
dominating_comm_cost = [comm_cost[i] for i in dominating_indices]
values = list(zip(dominating_comm_cost, dominating_complexity))

values.sort(key=lambda val: -val[1])
values.sort(key=lambda val: val[0])
values = [np.array(value) for value in values]

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

estimated_pareto = pd.DataFrame({'comm_cost': x, 'complexity': y})
file_util.save_pandas_csv(estimated_pareto, 'estimated_pareto.csv')

pareto_points = np.array(list(zip(x, y)))


with ProcessPool(nodes=setup.processes) as pool:
    comm_cost = list(main_data['comm_cost'].values)
    complexity = list(main_data['complexity'].values)
    points = np.array(list(zip(comm_cost, complexity)))
    distances = pool.map(lambda point: calculate_min_distance(pareto_points, point), points)
    main_data['pareto_closeness'] = distances

file_util.save_pandas_csv(main_data, 'main_data.csv')


plot = (pn.ggplot(pn.aes(x='comm_cost', y='complexity')) +
        pn.geom_line(size=1, data=estimated_pareto) +
        pn.geom_point(pn.aes(color='naturalness'), size=1.0, stroke=0.0, alpha=1.0, data=main_data) +
        pn.scale_color_cmap('cividis'))
plot.save('naturalness_with_pareto.png', width=6, height=4, dpi=300)


def standardize(data, cols):
    for col in cols:
        data[col] = (data[col] - data[col].mean()) / data[col].std()

main_data['optimality'] = 1 - main_data['pareto_closeness']

standardize(main_data,
            ['pareto_closeness', 'naturalness', 'monotonicity', 'conservativity', 'optimality'])

model = smf.ols(formula='pareto_closeness ~ naturalness', data=main_data)
results = model.fit()
print(results.summary())
print(results.pvalues)

model = smf.ols(formula='optimality ~ naturalness', data=main_data)
results = model.fit()
print(results.summary())
print(results.pvalues)