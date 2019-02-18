import json
import pickle
import Generator
import Parser

# with open('results/GeneratedQuantifiers.json') as json_file:
#     data = json.load(json_file)
#
# generated_quantifier_specs = data['quantifiers']
# generated_quantifiers = list(Parser.parse_quantifiers(generated_quantifier_specs).values())
#
universe_size = 40

universe = Generator.generate_simplified_models(universe_size)

# generated_meanings = [tuple([quantifier.evaluate(model) for model in universe]) for quantifier in generated_quantifiers]
#
# with open('results/generated_meanings.pickle', 'wb') as file:
#     pickle.dump(generated_meanings, file)


with open('EnglishQuantifiers.json') as json_file:
    data = json.load(json_file)

quantifier_specs = data['quantifiers']
quantifiers = Parser.parse_quantifiers(quantifier_specs)

meanings = {name: tuple([quantifier.evaluate(model) for model in universe]) for (name,quantifier) in quantifiers.items()}

with open('results/lexicalized_meanings.pickle', 'wb') as file:
    pickle.dump(meanings, file)
