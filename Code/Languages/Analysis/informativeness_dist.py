import os

import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('informativeness_strategy')

(args, setup, file_util) = analysisutil.init()
strategy = args.informativeness_strategy

informativeness = file_util.load_dill('informativeness_{0}.dill'.format(strategy))

fig = plt.figure()
plt.hist(informativeness)
plt.xlabel('informativeness')
plt.show()

filename = 'informativeness_{0}_hist.png'.format(strategy)
file_util.save_figure(fig,filename)
