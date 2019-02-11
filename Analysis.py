import numpy as np
import json

with open('./data/generated_quantifiers.txt') as file:
    generated_names = [line.rstrip('\n') for line in file]

generated_cost = np.loadtxt('./data/generated_quantifiers_cost.txt')
generated_complexity = np.loadtxt('./data/generated_quantifiers_complexity.txt')

quantifiers = zip(generated_names, generated_cost, generated_complexity)

optimized_quantifiers = []

for (name, cost, complexity) in quantifiers:
    if cost + complexity < .5:
        optimized_quantifiers.append((name, cost, complexity))

with open('./data/optimized_quantifiers.json', 'w') as file:
    json.dump(optimized_quantifiers, file, indent=4)
