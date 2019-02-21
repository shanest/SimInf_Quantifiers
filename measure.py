import json
import pickle
import numpy as np

import Generator
import Measurer
import Parser
import matplotlib.pyplot as plt

from ExperimentSetups import setup_1

measure_informativeness_relatively = True
separate_presupposition = False
max_quantifier_length = 4
model_size = 20
setup = setup_1

quantifiers = Parser.load_from_file(setup.lexical_quantifiers_filename, setup)

folderName = "{0}_length={1}_size={2}".format(setup.name,max_quantifier_length,model_size)
generated_quantifiers = list(Parser.load_from_file("results/{0}/GeneratedQuantifiers.json".format(folderName), setup).values())

with open('results/{0}/generated_meanings.pickle'.format(folderName),'rb') as file:
    generated_meanings = pickle.load(file)

with open('results/lexicalized_meanings/{0}_size={1}.pickle'.format(setup.name,model_size),'rb') as file:
    meanings = pickle.load(file)

presupposed_quantifiers = []
non_presupposed_quantifiers = []
presupposed_meanings = []
non_presupposed_meanings = []

for (quantifier,meaning) in zip(generated_quantifiers, generated_meanings):
    if quantifier.has_presupposition:
        presupposed_quantifiers.append(quantifier)
        presupposed_meanings.append(meaning)
    else:
        non_presupposed_quantifiers.append(quantifier)
        non_presupposed_meanings.append(meaning)

universe = Generator.generate_simplified_models(model_size)

measure_communicative_cost = Measurer.measure_relative_communicative_cost if measure_informativeness_relatively \
    else Measurer.measure_communicative_cost

# Measure cost and complexity for non-generated quantifiers

cost = {}
complexity = {}
for ((name, quantifier), meaning) in zip(quantifiers.items(), meanings.values()):
    cost[name] = measure_communicative_cost(meaning)
    complexity[name] = Measurer.measure_complexity(quantifier)
    plt.annotate(name, (cost[name], complexity[name]))


def measure(quantifiers, meanings):
    cost = []
    complexity = []
    for (quantifier, meaning) in zip(quantifiers, meanings):
        cost.append(measure_communicative_cost(meaning))
        complexity.append(Measurer.measure_complexity(quantifier))
    return cost,complexity


# Measure cost and complexity for generated quantifiers
(non_presupposed_cost, non_presupposed_complexity) = measure(non_presupposed_quantifiers,non_presupposed_meanings)
(presupposed_cost, presupposed_complexity) = measure(presupposed_quantifiers,presupposed_meanings)
(generated_cost, generated_complexity) = measure(generated_quantifiers,generated_meanings)



# Write results
with open('./results/lexicalized_quantifiers_cost/{0}_size={1}.txt'.format(setup.name,model_size), 'w') as f:
    for (name,value) in cost.items():
        f.write("{0}: {1}\n".format(name, value))

with open('./results/lexicalized_quantifiers_complexity/{0}_size={1}.txt'.format(setup.name,model_size), 'w') as f:
    for (name,value) in complexity.items():
        f.write("{0}: {1}\n".format(name, value))

with open('./results/{0}/generated_quantifiers.txt'.format(folderName), 'w') as f:
    for quantifier in generated_quantifiers:
        f.write("{0}\n".format(quantifier))

np.savetxt('./results/{0}/generated_quantifiers_cost.txt'.format(folderName), generated_cost)
np.savetxt('./results/{0}/generated_quantifiers_complexity.txt'.format(folderName), generated_complexity)

# Plot
plt.plot(presupposed_cost,presupposed_complexity,'o',color='red')
plt.plot(non_presupposed_cost,non_presupposed_complexity,'o',color='grey')
plt.plot(cost.values(),complexity.values(),'o')

# for i in range(len(generated_quantifier_expressions)):
#     plt.annotate(str(i),(generated_cost[i],generated_complexity[i]))

plt.axis([0,1,0,1])
plt.show()