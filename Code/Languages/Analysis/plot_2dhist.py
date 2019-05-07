import pygmo

import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('complexity_strategy')
analysisutil.add_argument('informativeness_strategy')

(args, setup, file_util) = analysisutil.init()

informativeness = file_util.load_dill('informativeness_{0}.dill'.format(args.informativeness_strategy))
complexity = file_util.load_dill('complexity_{0}.dill'.format(args.complexity_strategy))

fig = plt.figure()
plt.hist2d(informativeness,complexity,range=[[0,.26],[0,1]],bins=30,cmin=1)

plt.colorbar()
plt.xlabel('informativeness')
plt.ylabel('complexity')

plt.show()

file_util.save_figure(fig, '{0}_{1}_hist2d'.format(
    args.complexity_strategy,
    args.informativeness_strategy
))