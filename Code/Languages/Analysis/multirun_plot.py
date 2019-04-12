import pygmo

import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('complexity_strategy')
analysisutil.add_argument('informativeness_strategy')
analysisutil.add_argument('run_names', nargs='+')

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

fig = plt.figure()

for run_name in args.run_names:
    informativeness = file_util.load_dill('{0}/informativeness_{1}.dill'.format(run_name, args.informativeness_strategy))
    complexity = file_util.load_dill('{0}/complexity_{1}.dill'.format(run_name, args.complexity_strategy))
    plt.plot(informativeness, complexity, 'o', label=run_name)

plt.legend()
plt.xlabel('informativeness')
plt.ylabel('complexity')

plt.show()

file_util.save_figure(fig, '{0}_{1}_multirun_plot'.format(
    args.complexity_strategy,
    args.informativeness_strategy
))