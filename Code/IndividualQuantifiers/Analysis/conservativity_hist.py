import analysisutil
import matplotlib.pyplot as plt

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

monotonicities = file_util.load_dill('conservativity_max.dill')

fig = plt.figure()

plt.hist(monotonicities)

plt.show()
file_util.save_figure(fig, 'monotonicity_hist')
