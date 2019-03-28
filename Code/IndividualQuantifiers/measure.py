import argparse
import os

import dill
import numpy as np

import Parser, Measurer, ExperimentSetups
import matplotlib.pyplot as plt
from pathos.pools import ProcessPool

from Quantifier import Quantifier

parser = argparse.ArgumentParser(description="Generate Quantifiers")
parser.add_argument('setup', help='Path to the setup json file.')
parser.add_argument('max_quantifier_length', type=int)
parser.add_argument('model_size', type=int)
parser.add_argument('--dest_dir', default='results')
parser.add_argument('--processes', default=4, type=int)
parser.add_argument('--relative', default=False, action="store_true")
parser.add_argument('--no_presupp', dest="use_presuppositions", default=True, action="store_false")


args = parser.parse_args()

measure_informativeness_relatively = args.relative
max_quantifier_length = args.max_quantifier_length
model_size = args.model_size
setup = ExperimentSetups.parse(args.setup)

quantifiers = Parser.load_from_file(setup.lexical_quantifiers_filename, setup)

folderName = "{0}/{1}_length={2}_size={3}".format(args.dest_dir,setup.name,max_quantifier_length,model_size)

if args.use_presuppositions:
    with open('{0}/generated_quantifiers.dill'.format(folderName),'rb') as file:
        generated_quantifiers = dill.load(file)

    with open('{0}/generated_meanings.dill'.format(folderName),'rb') as file:
        generated_meanings = dill.load(file)
else:
    with open('{0}/generated_expressions.dill'.format(folderName),'rb') as file:
        expressions_by_meaning = dill.load(file)

    generated_quantifiers = [Quantifier(e) for e in expressions_by_meaning.values()]
    generated_meanings = list(expressions_by_meaning.keys())

with open('{0}/lexicalized_meanings/{1}_size={2}.dill'.format(args.dest_dir,setup.name,model_size),'rb') as file:
    meanings = dill.load(file)

universe = setup.generate_models(model_size)

measure_communicative_cost = Measurer.measure_relative_communicative_cost if measure_informativeness_relatively \
    else Measurer.measure_communicative_cost

# Measure cost and complexity for non-generated quantifiers

cost = {}
complexity = {}
for (name, quantifier) in quantifiers.items():
    meaning = meanings[name]
    cost[name] = measure_communicative_cost(meaning)
    complexity[name] = setup.measure_quantifier_complexity(quantifier)
    plt.annotate(name, (cost[name], complexity[name]))


def measure(quantifiers, meanings):
    p = ProcessPool(nodes=args.processes)
    cost = p.map(measure_communicative_cost,meanings)
    complexity  = p.map(setup.measure_quantifier_complexity,quantifiers)
    return cost, complexity


(generated_cost, generated_complexity) = measure(generated_quantifiers, generated_meanings)


# Write results
os.makedirs('{0}/lexicalized_quantifiers_cost'.format(args.dest_dir), exist_ok=True)
with open('{0}/lexicalized_quantifiers_cost/{1}_size={2}.txt'.format(args.dest_dir,setup.name,model_size), 'w') as f:
    for (name,value) in cost.items():
        f.write("{0}: {1}\n".format(name, value))

os.makedirs('{0}/lexicalized_quantifiers_complexity'.format(args.dest_dir), exist_ok=True)
with open('{0}/lexicalized_quantifiers_complexity/{1}_size={2}.txt'.format(args.dest_dir,setup.name,model_size), 'w') as f:
    for (name,value) in complexity.items():
        f.write("{0}: {1}\n".format(name, value))

with open('{0}/generated_quantifiers.txt'.format(folderName), 'w') as f:
    for quantifier in generated_quantifiers:
        f.write("{0}\n".format(quantifier))

np.savetxt('{0}/generated_quantifiers_cost.txt'.format(folderName), generated_cost)
np.savetxt('{0}/generated_quantifiers_complexity.txt'.format(folderName), generated_complexity)


# Split by presupposition
presupposed_cost = []
presupposed_complexity = []
non_presupposed_cost = []
non_presupposed_complexity = []

for quantifier, g_cost, g_complexity in zip(generated_quantifiers, generated_cost, generated_complexity):
    if quantifier.has_presupposition:
        presupposed_cost.append(g_cost)
        presupposed_complexity.append(g_complexity)
    else:
        non_presupposed_cost.append(g_cost)
        non_presupposed_complexity.append(g_complexity)

# Plot
plt.plot(presupposed_cost,presupposed_complexity,'o',color='red')
plt.plot(non_presupposed_cost,non_presupposed_complexity,'o',color='grey')
plt.plot(cost.values(),complexity.values(),'o')

# for i in range(len(generated_quantifier_expressions)):
#     plt.annotate(str(i),(generated_cost[i],generated_complexity[i]))

plt.axis([0,1,0,1])
plt.savefig("{0}/plot.png".format(folderName), bbox_inches='tight')