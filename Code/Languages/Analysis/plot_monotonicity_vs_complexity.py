import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('complexity_strategy')

(args, setup, file_util) = analysisutil.init()

complexity = file_util.load_dill('complexity_{0}.dill'.format(args.complexity_strategy))
monotonicity = file_util.load_dill('monotonicity.dill')

fig = plt.figure()
plt.scatter(monotonicity, complexity)

plt.ylabel('complexity')
plt.xlabel('monotonicity')

plt.show()

file_util.save_figure(fig, '{0}_plot_monotonicity'.format(
    args.complexity_strategy
))
