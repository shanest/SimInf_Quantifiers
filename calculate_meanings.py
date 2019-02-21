import os
import pickle
import Parser
from ExperimentSetups import setup_1

setup = setup_1
model_size = 20

universe = setup.generate_models(model_size)

quantifiers = Parser.load_from_file(setup.lexical_quantifiers_filename, setup)

meanings = {name: tuple([quantifier.evaluate(model) for model in universe]) for (name,quantifier) in quantifiers.items()}

os.makedirs('results/lexicalized_meanings', exist_ok=True)
with open('results/lexicalized_meanings/{0}_size={1}.pickle'.format(setup.name,model_size), 'wb') as file:
    pickle.dump(meanings, file)
