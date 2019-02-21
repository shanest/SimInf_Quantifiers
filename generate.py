import json
import os
import pickle
import Generator

# Parameters
from ExperimentSetups import setup_1
from Quantifier import Quantifier

setup = setup_1
max_quantifier_length = 4
model_size = 20

# Generate quantifiers
# generated_quantifiers, generated_meanings = \
#     Generator.generate_unique_quantifiers(
#         designated_quantifier_lengths,
#         quantifiers_per_length,
#         presupposition_lengths,
#         presupposition_per_length_combination,
#         model_size,
#         universe
#     )


universe = setup.generate_models(model_size)

(generated_expressions_dict, expressions_by_meaning) = Generator.generate_all_expressions(setup_1,max_quantifier_length,model_size,universe)

generated_expressions = list(expressions_by_meaning[bool].values())

generated_quantifiers = [Quantifier(expression) for expression in generated_expressions]

os.makedirs("results/{0}".format(folderName), exist_ok=True)

with open('results/{0}/GeneratedQuantifiers.json'.format(folderName), 'w') as file:
    gq_dict = {"{0}".format(i): quantifier.to_name_structure() for (i, quantifier) in enumerate(generated_quantifiers)}
    json.dump({'quantifiers': gq_dict}, file, indent=2)

with open('results/{0}/generated_meanings.pickle'.format(folderName), 'wb') as file:
    pickle.dump(list(expressions_by_meaning[bool].keys()), file)

with open('./results/{0}/generated_quantifiers.txt'.format(folderName), 'w') as f:
    for quantifier in generated_quantifiers:
        f.write("{0}\n".format(quantifier))

print('Generation finished')
