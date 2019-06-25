import dill

import Measurer
import Parser
import analysisutil
import matplotlib.pyplot as plt

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

monotonicities_a_up = file_util.load_dill('monotonicities_a_up.dill')
monotonicities_a_down = file_util.load_dill('monotonicities_a_down.dill')
monotonicities_b_up = file_util.load_dill('monotonicities_b_up.dill')
monotonicities_b_down = file_util.load_dill('monotonicities_b_down.dill')

monotonicities_a = list(map(max, monotonicities_a_up, monotonicities_a_down))
monotonicities_b = list(map(max, monotonicities_b_up, monotonicities_b_down))

fig = plt.figure()

# Plot
plt.hist2d(monotonicities_a,monotonicities_b,bins=20)
plt.colorbar()

# for i in range(len(generated_quantifier_expressions)):
#     plt.annotate(str(i),(generated_cost[i],generated_complexity[i]))

plt.xlabel('a')
plt.ylabel('b')
plt.show()
file_util.save_figure(fig, 'monotonicity_a_vs_b_plot')
