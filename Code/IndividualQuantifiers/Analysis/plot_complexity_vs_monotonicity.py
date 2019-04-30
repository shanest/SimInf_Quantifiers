import dill

import Measurer
import Parser
import analysisutil
import matplotlib.pyplot as plt

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

complexities = file_util.load_dill('expression_complexities.dill')
monotonicities = file_util.load_dill('monotonicities_max.dill')

fig = plt.figure()

# Plot
plt.plot(monotonicities,complexities,'o')

# for i in range(len(generated_quantifier_expressions)):
#     plt.annotate(str(i),(generated_cost[i],generated_complexity[i]))

plt.xlabel('monotonicity')
plt.ylabel('length')
plt.show()
file_util.save_figure(fig, 'monotonicity_complexity_plot')
