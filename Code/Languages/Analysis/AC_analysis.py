from pathos.multiprocessing import ProcessPool
# import analysisutil
# from Languages import LanguageLoader
import dill
import pandas as pd
import numpy as np
from numpy.linalg import norm
import pygmo
import statsmodels.formula.api as smf

from plotnine import *

with open('../../../results/Final_length=12_size=10/27_may_evo_2000_100gens_3mutations_10words/complexity_wordcomplexity.dill', 'rb') as f:
    evo_comp = dill.load(f)

with open('../../../results/Final_length=12_size=10/27_may_evo_2000_100gens_3mutations_10words/informativeness_simmax.dill', 'rb') as f:
    evo_inf = dill.load(f)

pareto_data = pd.DataFrame(
    {'complexity': evo_comp,
     'comm_cost': [1-x for x in evo_inf]}
)

main_data = pd.read_csv('../../../results/Final_length=12_size=10/tables/pandas_27_may_natural_degrees.csv')

comm_cost = list(pareto_data['comm_cost'].values) + list(main_data['comm_cost'].values)
complexity = list(pareto_data['complexity'].values) + list(main_data['complexity'].values)

dominating_indices = pygmo.non_dominated_front_2d(
    list(zip(complexity, comm_cost)))
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

estimated_pareto = pd.DataFrame({'comm_cost':x, 'complexity':y})

plot = (ggplot(aes(x='comm_cost', y='complexity')) +
        geom_line(size=1, data=estimated_pareto) +
        geom_point(aes(color='naturalness'), size=1.0, stroke=0.0, alpha=1.0, data=main_data) +
        scale_color_cmap('cividis'))
plot.save('naturalness_with_pareto.png', width=6, height=4, dpi=300)


def standardize(data, cols):
    for col in cols:
        data[col] = (data[col] - data[col].mean()) / data[col].std()


standardize(main_data,
            ['pareto_closeness', 'naturalness', 'monotonicity', 'conservativity'])

model = smf.ols(formula='pareto_closeness ~ naturalness', data=main_data)
results = model.fit()
print(results.summary())
print(results.pvalues)
