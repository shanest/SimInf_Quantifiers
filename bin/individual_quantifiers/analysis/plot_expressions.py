import dill
import matplotlib.pyplot as plt

from siminf import measurer
from siminf import parser 
from siminf import analysisutil

# def main():

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

generated_comp = file_util.load_dill('expression_complexities.dill')
generated_cost = file_util.load_dill('expression_costs.dill')

lexicalized_quantifiers = parser.load_from_file(setup.lexical_quantifiers_filename, setup)

with open('{0}/lexicalized_meanings/{1}_size={2}.dill'.format(args.dest_dir,setup.name,args.model_size),'rb') as file:
    meanings = dill.load(file)

fig = plt.figure()

cost = {}
complexity = {}
for (name, quantifier) in lexicalized_quantifiers.items():
    if quantifier.has_presupposition:
        continue
    meaning = meanings[name]
    cost[name] = measurer.measure_communicative_cost(meaning)
    complexity[name] = setup.measure_expression_complexity(quantifier.expression, args.max_quantifier_length)
    plt.annotate(name, (cost[name], complexity[name]))

# Plot
plt.plot(generated_cost,generated_comp,'o',color='grey')
plt.plot(cost.values(),complexity.values(),'o')

# for i in range(len(generated_quantifier_expressions)):
    # plt.annotate(str(i),(generated_cost[i],generated_complexity[i]))

plt.axis([0,1,0,1])
plt.xlabel('communicative cost')
plt.ylabel('complexity')
plt.show()
file_util.save_figure(fig, 'expression_plot')

print('plot_expressions.py finished.')

# if __name__ == "__main__":
#     main()