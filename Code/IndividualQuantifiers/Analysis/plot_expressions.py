import dill

import Measurer
import Parser
import analysisutil
import matplotlib.pyplot as plt

(args, setup, file_util) = analysisutil.init()

generated_comp = file_util.load_dill('expression_complexities.dill')
generated_cost = file_util.load_dill('expression_costs.dill')

lexicalized_quantifiers = Parser.load_from_file(setup.lexical_quantifiers_filename, setup)

with open('{0}/lexicalized_meanings/{1}_size={2}.dill'.format(args.dest_dir,setup.name,args.model_size),'rb') as file:
    meanings = dill.load(file)

fig = plt.figure()

cost = {}
complexity = {}
for (name, quantifier) in lexicalized_quantifiers.items():
    if quantifier.has_presupposition:
        continue
    meaning = meanings[name]
    cost[name] = Measurer.measure_communicative_cost(meaning)
    complexity[name] = setup.measure_quantifier_complexity(quantifier)
    plt.annotate(name, (cost[name], complexity[name]))

# Plot
plt.plot(generated_cost,generated_comp,color='grey')
plt.plot(cost.values(),complexity.values(),'o')

# for i in range(len(generated_quantifier_expressions)):
#     plt.annotate(str(i),(generated_cost[i],generated_complexity[i]))

plt.axis([0,1,0,1])
plt.show()
file_util.save_figure(fig, 'expression_plot')
