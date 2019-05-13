import analysisutil
import statsmodels.formula.api as smf

analysisutil.add_argument('table_name')
analysisutil.add_argument('natural_run')
analysisutil.add_argument('random_run')

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

df = file_util.load_pandas_csv("pandas_{0}.csv".format(args.table_name))

df = df[df.apply(lambda row: row.run in [args.natural_run, args.random_run], axis=1)]

df['natural'] = list(map(lambda run_name: 1 if run_name == args.natural_run else 0, df['run'].values))

print(df.head())

model = smf.ols(formula='pareto_closeness ~ natural + monotonicity', data=df)
result = model.fit()

print(result.summary())
