import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('set')
(args, setup, file_util) = analysisutil.init(use_base_dir=True)

monotonicities_a_up = file_util.load_dill('monotonicities_{0}_up.dill'.format(args.set))
monotonicities_a_down = file_util.load_dill('monotonicities_{0}_down.dill'.format(args.set))

monotonicities = list(map(max,monotonicities_a_down,monotonicities_a_up))

fig = plt.figure()

plt.hist(monotonicities, bins=30)

plt.show()
file_util.save_figure(fig, 'monotonicity_{0}_hist'.format(args.set))
