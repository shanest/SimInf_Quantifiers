import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('complexity_strategy')

(args, setup, file_util) = analysisutil.init()
strategy = args.complexity_strategy

complexity = file_util.load_dill('complexity_{0}.dill'.format(strategy))

fig = plt.figure()
plt.hist(complexity)
plt.xlabel('complexity')
plt.show()

filename = 'complexity_{0}_hist.png'.format(strategy)
file_util.save_figure(fig, filename)
