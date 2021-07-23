import scipy
import pandas as pd
import numpy as np
import plotnine as pn
import statsmodels.formula.api as smf
from siminf import analysisutil

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

natural_data = file_util.load_pandas_csv('natural_data.csv')
random_data = file_util.load_pandas_csv('random_data.csv')
pareto_data = file_util.load_pandas_csv('estimated_pareto.csv')


def make_plot(data, color_variable, filename):
    plot = (pn.ggplot(pn.aes(x='comm_cost', y='complexity')) +
            pn.geom_line(size=1, data=pareto_data) +
            pn.geom_point(pn.aes(color=color_variable), size=1.0, stroke=0.0, alpha=1.0, data=data) +
            pn.scale_color_cmap('cividis'))
    file_util.save_plot(plot, filename, width=6, height=4, dpi=300)

"""
make_plot(natural_data, 'naturalness', 'naturalness_with_pareto.png')
make_plot(random_data, 'monotonicity', 'monotonicity_with_pareto.png')
make_plot(random_data, 'conservativity', 'conservativity_with_pareto.png')
"""

def standardize(data, cols):
    for col in cols:
        data[col] = (data[col] - data[col].mean()) / data[col].std()


def fit_stat_model(formula, data):
    model = smf.ols(formula=formula, data=data)
    results = model.fit()
    print(results.summary())
    print(results.pvalues)


def full_analysis(data, predictors, num_bootstrap_samples=5000):
    data['optimality'] = 1 - data['pareto_closeness']

    # standardize(data, predictors + ['pareto_closeness', 'optimality'])

    for predictor in predictors:
        print(predictor)
        r, _ = scipy.stats.pearsonr(data['optimality'], data[predictor])
        print(r)
        for bootstrap_sample_percent in np.geomspace(0.01, 1.0, num=5):
            rs = []
            for _ in range(num_bootstrap_samples):
                bootstrap_sample = data.sample(n=int(bootstrap_sample_percent*len(data)), replace=True)
                r, _ = scipy.stats.pearsonr(bootstrap_sample['optimality'], bootstrap_sample[predictor])
                rs.append(r)
            print(scipy.stats.scoreatpercentile(rs, (2.5, 97.5)))


predictors = ['monotonicity', 'conservativity']
print('random data')
full_analysis(random_data, predictors)
print()
print('natural data')
full_analysis(natural_data, predictors + ['naturalness'])