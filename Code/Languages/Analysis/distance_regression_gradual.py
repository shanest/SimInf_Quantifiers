import analysisutil
import statsmodels.formula.api as smf

analysisutil.add_argument('table_name')

(args, setup, file_util) = analysisutil.init()
file_util_base = file_util.get_base_file_util()

df = file_util_base.load_pandas_csv("pandas_{0}.csv".format(args.table_name))

print(df.head())

model = smf.ols(formula='pareto_closeness ~ naturalness * monotonicity', data=df)
result = model.fit()

print(result.summary())
