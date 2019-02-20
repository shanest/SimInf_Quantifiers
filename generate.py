import json
import pickle
import Generator

# Parameters
model_size = 40
designated_quantifier_lengths = [2, 3, 4, 5, 6, 7, 8]
quantifiers_per_length = 200
generate_new_quantifiers = True
presupposition_per_length_combination = 0
presupposition_lengths = [2, 3, 4, 5]

if presupposition_per_length_combination * len(presupposition_lengths) > quantifiers_per_length:
    raise ValueError('More presuppositions required than desired amount of quantifiers')

universe = Generator.generate_simplified_models(model_size)

# Generate quantifiers
generated_quantifiers, generated_meanings = \
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

with open('results/generated_meanings.pickle', 'wb') as file:
    pickle.dump(generated_meanings, file)

print('Generation finished')
