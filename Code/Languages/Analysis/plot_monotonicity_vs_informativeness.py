import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('informativeness_strategy')

(args, setup, file_util) = analysisutil.init()

informativeness = file_util.load_dill('informativeness_{0}.dill'.format(args.informativeness_strategy))
monotonicity = file_util.load_dill('monotonicity.dill')

fig = plt.figure()
plt.scatter(monotonicity, informativeness)

plt.ylabel('informativeness')
plt.xlabel('monotonicity')

plt.show()

file_util.save_figure(fig, '{0}_plot_monotonicity'.format(
    args.informativeness_strategy
))
