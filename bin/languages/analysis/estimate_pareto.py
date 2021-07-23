from pathos.multiprocessing import ProcessPool
import pandas as pd
import numpy as np
from numpy.linalg import norm
import pygmo
import plotnine as pn
from siminf import analysisutil
import statsmodels.formula.api as smf
import scipy

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


natural_data = load_data(file_util.get_sub_file_util(setup.natural_name), setup.comp_strat, setup.inf_strat)
random_data = load_data(file_util.get_sub_file_util(setup.random_name), setup.comp_strat, setup.inf_strat)
pareto_data = load_data(file_util.get_sub_file_util(setup.pareto_name), setup.comp_strat, setup.inf_strat)


# combine complexities and costs
complexity = list(pareto_data['complexity'].values) + list(natural_data['complexity'].values) + list(random_data['complexity'].values)
comm_cost = list(pareto_data['comm_cost'].values) + list(natural_data['comm_cost'].values) + list(random_data['comm_cost'].values)


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
values = list(set(zip(dominating_comm_cost, dominating_complexity)))

values.sort(key=lambda val: -val[1])
values.sort(key=lambda val: val[0])
values.append((1.0, 0.0))  # TODO: avoid this hack?

pareto_x, pareto_y = list(zip(*values))
interpolated = scipy.interpolate.interp1d(pareto_x, pareto_y)

pareto_costs = np.linspace(pareto_x[0], pareto_x[-1], num=5000)
pareto_complexities = interpolated(pareto_costs)


"""
pareto_x, pareto_y = list(zip(*values))
print(pareto_x)
print(pareto_y)

def frontier_complexity(comm_cost, a, b):
    # Curve to estimate frontier.
    return a * comm_cost ** b

(opta, optb), _ = scipy.optimize.curve_fit(frontier_complexity, pareto_x, pareto_y)

print(opta, optb)

pareto_costs = np.linspace(0.72, 1.0, num=5000)
pareto_complexities = frontier_complexity(pareto_costs, opta, optb)

"""

estimated_pareto = pd.DataFrame({'comm_cost': pareto_costs, 'complexity': pareto_complexities})
file_util.save_pandas_csv(estimated_pareto, 'estimated_pareto.csv')


pareto_points = np.array(list(zip(pareto_costs, pareto_complexities)))

def measure_closeness(data, pareto_frontier):
    with ProcessPool(nodes=setup.processes) as pool:
        comm_cost = list(data['comm_cost'].values)
        complexity = list(data['complexity'].values)
        points = np.array(list(zip(comm_cost, complexity)))
        distances = pool.map(lambda point: calculate_min_distance(pareto_frontier, point), points)
        data['pareto_closeness'] = distances

measure_closeness(natural_data, pareto_points)
measure_closeness(random_data, pareto_points)

file_util.save_pandas_csv(natural_data, 'natural_data.csv')
file_util.save_pandas_csv(random_data, 'random_data.csv')