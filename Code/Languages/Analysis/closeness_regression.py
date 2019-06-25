import statsmodels

import analysisutil
import statsmodels.formula.api as smf
import plotnine as pn

analysisutil.add_argument('table_name')
analysisutil.add_argument('natural_run')
analysisutil.add_argument('random_run')

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

df = file_util.load_pandas_csv("pandas_{0}.csv".format(args.table_name))

df = df[df.apply(lambda row: row.run in [args.natural_run, args.random_run], axis=1)]

def standardize(series):
    return (series - series.mean()) / series.std()


df['conservativity'] = standardize(df['conservativity'])
df['monotonicity'] = standardize(df['monotonicity'])

df['natural'] = list(map(lambda run_name: 1 if run_name == args.natural_run else 0, df['run'].values))
df['natural'] = df['natural'].astype('category')

print(df.head())

df_natural = df[df['natural'] == 1]

#plt = (pn.ggplot(df_natural, pn.aes('pareto_closeness')) +
        # pn.geom_density() +
       # pn.geom_density(data=df[df['natural'] == 0], color='r'))

#print(plt)

natural = df[df.apply(lambda row: row.run == args.natural_run, axis=1)]['pareto_closeness']
non_natural = df[df.apply(lambda row: row.run == args.random_run, axis=1)]['pareto_closeness']

print(natural.mean())
print(natural.std())
print(non_natural.mean())
print(non_natural.std())

results = statsmodels.stats.weightstats.ttest_ind(natural,non_natural,alternative="two-sided",usevar="unequal")
print(results)

def fit(formula):
    model = smf.ols(formula=formula, data=df)
    result = model.fit()

    print(result.summary())
    print(result.pvalues)


fit('pareto_closeness ~ natural*monotonicity')
fit('pareto_closeness ~ natural*monotonicity*conservativity')
fit('pareto_closeness ~ natural')
fit('pareto_closeness ~ monotonicity')
fit('pareto_closeness ~ natural + monotonicity + conservativity')
