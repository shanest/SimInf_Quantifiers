import numpy as np
import matplotlib.pyplot as plt
import json
import Generator
import Parser
import Measurer

# Parameters
model_size = 20
designated_quantifier_lengths = [2,3,4,5,6,7,8]
quantifiers_per_length = 50
generate_new_quantifiers = True
measure_informativeness_relatively = True
presupposition_per_length_combination = 4
presupposition_lengths = [2,3,4,5]

measure_communicative_cost = Measurer.measure_relative_communicative_cost if measure_informativeness_relatively \
    else Measurer.measure_communicative_cost

if presupposition_per_length_combination * len(presupposition_lengths) > quantifiers_per_length:
    raise ValueError('More presuppositions required than desired amount of quantifiers')

universe = Generator.generate_models(model_size)

# Read lexicalized quantifiers from data file
with open('EnglishQuantifiers.json') as json_file:
    data = json.load(json_file)

quantifier_specs = data['quantifiers']
quantifiers = Parser.parse_quantifiers(quantifier_specs)

# Generate quantifiers
if generate_new_quantifiers:
    generated_quantifiers = \
        Generator.generate_unique_quantifiers(
            designated_quantifier_lengths,
            quantifiers_per_length,
            presupposition_lengths,
            presupposition_per_length_combination,
            model_size,
            universe
        )

    with open('results/GeneratedQuantifiers.json', 'w') as file:
        gq_dict = {"{0}".format(i): quantifier.to_name_structure() for (i, quantifier) in enumerate(generated_quantifiers)}
        json.dump({'quantifiers': gq_dict}, file, indent=2)

    print('Generation finished')

else:
    with open('results/GeneratedQuantifiers.json') as json_file:
        data = json.load(json_file)

    generated_quantifier_specs = data['quantifiers']
    generated_quantifiers = Parser.parse_quantifiers(generated_quantifier_specs).values()

# Measure cost and complexity for non-generated quantifiers

cost = {}
complexity = {}
for name, quantifier in quantifiers.items():
    cost[name] = measure_communicative_cost(quantifier,universe)
    complexity[name] = Measurer.measure_complexity(quantifier)
    plt.annotate(name,(cost[name],complexity[name]))

# Measure cost and complexity for generated quantifiers
generated_cost = []
generated_complexity = []
for quantifier in generated_quantifiers:
    generated_cost.append(measure_communicative_cost(quantifier,universe))
    generated_complexity.append(Measurer.measure_complexity(quantifier))


# Write results
with open('./results/lexicalized_quantifiers_cost.txt', 'w') as f:
    for (name,value) in cost.items():
        f.write("{0}: {1}\n".format(name, value))

with open('./results/lexicalized_quantifiers_complexity.txt', 'w') as f:
    for (name,value) in complexity.items():
        f.write("{0}: {1}\n".format(name, value))

with open('./results/generated_quantifiers.txt', 'w') as f:
    for quantifier in generated_quantifiers:
        f.write("{0}\n".format(quantifier))

np.savetxt('./results/generated_quantifiers_cost.txt',generated_cost)
np.savetxt('./results/generated_quantifiers_complexity.txt',generated_complexity)

# Plot
plt.plot(generated_cost,generated_complexity,'o',color='grey')
plt.plot(cost.values(),complexity.values(),'o')

# for i in range(len(generated_quantifier_expressions)):
#     plt.annotate(str(i),(generated_cost[i],generated_complexity[i]))

plt.axis([0,1,0,1])
plt.show()