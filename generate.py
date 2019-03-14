import json
import os
import pickle
import Generator

# Parameters
from ExperimentSetups import setup_1
from Quantifier import Quantifier

setup = setup_1
max_quantifier_length = 6
model_size = 20

universe = setup.generate_models(model_size)

(generated_expressions_dict, expressions_by_meaning) = Generator.generate_all_expressions(setup,max_quantifier_length,model_size,universe)

quantifiers_by_meaning = Generator.add_presuppositions(setup, expressions_by_meaning[bool])

generated_quantifiers = list(quantifiers_by_meaning.values())
generated_meanings = list(quantifiers_by_meaning.keys())

folderName = "{0}_length={1}_size={2}".format(setup.name,max_quantifier_length,model_size)

os.makedirs("results/{0}".format(folderName), exist_ok=True)

with open('results/{0}/GeneratedQuantifiers.json'.format(folderName), 'w') as file:
    gq_dict = {"{0}".format(i): quantifier.to_name_structure() for (i, quantifier) in enumerate(generated_quantifiers)}
    json.dump({'quantifiers': gq_dict}, file, indent=2)

with open('results/{0}/generated_meanings.pickle'.format(folderName), 'wb') as file:
    pickle.dump(generated_meanings, file)

with open('./results/{0}/generated_quantifiers.txt'.format(folderName), 'w') as f:
    for quantifier in generated_quantifiers:
        f.write("{0}\n".format(quantifier))

print('Generation finished')
