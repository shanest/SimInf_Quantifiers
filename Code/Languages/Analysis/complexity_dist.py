import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('complexity_strategy')

(args, setup, file_util) = analysisutil.init()

complexity = file_util.load_dill('complexity_{0}.dill'.format(args.complexity_strategy))

plt.hist(complexity)
plt.show()
