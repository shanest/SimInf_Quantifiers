import analysisutil
import statsmodels.formula.api as smf
import plotnine as pn

analysisutil.add_argument('table_name')

(args, setup, file_util) = analysisutil.init()
file_util_base = file_util.get_base_file_util()

df = file_util_base.load_pandas_csv("pandas_{0}.csv".format(args.table_name))

print(df.head())

def standardize(series):
    return (series - series.mean()) / series.std()


#df['conservativity'] = standardize(df['conservativity'])
#df['monotonicity'] = standardize(df['monotonicity'])
#df['naturalness'] = standardize(df['naturalness'])

#plt = (pn.ggplot(df, pn.aes('naturalness', 'pareto_closeness'))
#       + pn.geom_point()
#        + pn.stat_smooth(method='lm',color='r'))
#
#print(plt)

model = smf.ols(formula='pareto_closeness ~ naturalness', data=df)
result = model.fit()

print(result.summary())
print(result.pvalues)

model = smf.ols(formula='pareto_closeness ~ naturalness + monotonicity', data=df)
result = model.fit()

print(result.summary())
print(result.pvalues)

model = smf.ols(formula='pareto_closeness ~ naturalness + conservativity', data=df)
result = model.fit()

print(result.summary())
print(result.pvalues)

model = smf.ols(formula='pareto_closeness ~ conservativity + monotonicity', data=df)
result = model.fit()

print(result.summary())
print(result.pvalues)

model = smf.ols(formula='pareto_closeness ~ naturalness + monotonicity + conservativity', data=df)
result = model.fit()

print(result.summary())
print(result.pvalues)