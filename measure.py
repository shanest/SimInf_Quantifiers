import json
import pickle
import numpy as np

import Generator
import Measurer
import Parser
import matplotlib.pyplot as plt

with open('EnglishQuantifiers.json') as json_file:
    data = json.load(json_file)

quantifier_specs = data['quantifiers']
quantifiers = Parser.parse_quantifiers(quantifier_specs)

with open('results/GeneratedQuantifiers.json') as json_file:
    data = json.load(json_file)

generated_quantifier_specs = data['quantifiers']
generated_quantifiers = Parser.parse_quantifiers(generated_quantifier_specs).values()

with open('results/generated_meanings.pickle','rb') as file:
    generated_meanings = pickle.load(file)

with open('results/lexicalized_meanings.pickle','rb') as file:
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

measure_informativeness_relatively = True
separate_presupposition = False
universe_size = 100

universe = Generator.generate_simplified_models(universe_size)

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
(generated_cost, generated_complexity) = measure(non_presupposed_quantifiers,non_presupposed_meanings)
(presupposed_cost, presupposed_complexity) = measure(presupposed_quantifiers,presupposed_meanings)



# Write results
# with open('./results/lexicalized_quantifiers_cost.txt', 'w') as f:
#     for (name,value) in cost.items():
#         f.write("{0}: {1}\n".format(name, value))
#
# with open('./results/lexicalized_quantifiers_complexity.txt', 'w') as f:
#     for (name,value) in complexity.items():
#         f.write("{0}: {1}\n".format(name, value))
#
# with open('./results/generated_quantifiers.txt', 'w') as f:
#     for quantifier in generated_quantifiers:
#         f.write("{0}\n".format(quantifier))
#
# np.savetxt('./results/generated_quantifiers_cost.txt',generated_cost)
# np.savetxt('./results/generated_quantifiers_complexity.txt',generated_complexity)

# Plot
plt.plot(presupposed_cost,presupposed_complexity,'o',color='red')
plt.plot(generated_cost,generated_complexity,'o',color='grey')
plt.plot(cost.values(),complexity.values(),'o')

# for i in range(len(generated_quantifier_expressions)):
#     plt.annotate(str(i),(generated_cost[i],generated_complexity[i]))

plt.axis([0,1,0,1])
plt.show()