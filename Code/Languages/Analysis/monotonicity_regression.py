import plotnine as pn
import analysisutil
from Languages import LanguageLoader
import statsmodels.formula.api as smf

analysisutil.add_argument('comp_strat')
analysisutil.add_argument('inf_strat')

(args, setup, file_util) = analysisutil.init()

data = LanguageLoader.load_pandas_table(file_util, args.comp_strat, args.inf_strat)

model_inf = smf.ols(formula='monotonicity ~ comm_cost', data=data)
model_comp = smf.ols(formula='monotonicity ~ complexity', data=data)
model_both = smf.ols(formula='monotonicity ~ complexity + comm_cost', data=data)
model = smf.ols(formula='monotonicity ~ complexity * comm_cost', data=data)

result_inf = model_inf.fit()
result_comp = model_comp.fit()
result_both = model_both.fit()
result = model.fit()

print(result_inf.summary())
print(result_comp.summary())
print(result_both.summary())
print(result.summary())
# plt = (pn.ggplot(data, pn.aes('comm_cost', 'complexity'))
#        + pn.geom_point()
#        + pn.stat_smooth(method='lm'))

# print(plt)
