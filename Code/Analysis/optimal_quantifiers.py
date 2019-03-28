import numpy as np
import Parser

quantifiers = list(Parser.load_from_file('../results/GeneratedQuantifiers.json').values())
costs = np.loadtxt('../results/generated_quantifiers_cost.txt')
complexities = np.loadtxt('../results/generated_quantifiers_complexity.txt')

universe_size = 20

optimal_quantifiers = []

for (quantifier, cost, complexity) in zip(quantifiers, costs, complexities):
    if cost < .1 and complexity < .2:
        print("{0}\ncost: {1}\ncomp: {2}".format(quantifier, cost, complexity))
