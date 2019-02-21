import json
import pickle
import Generator

# Parameters
from Quantifier import Quantifier

model_size = 20
primitive_set = 'TODO'

universe = Generator.generate_simplified_models(model_size)

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


(generated_expressions_dict, expressions_by_meaning) = Generator.generate_all_expressions(7,model_size,universe)

generated_expressions = list(expressions_by_meaning[bool].values())

generated_quantifiers = [Quantifier(expression) for expression in generated_expressions]

with open('results/GeneratedQuantifiers.json', 'w') as file:
    gq_dict = {"{0}".format(i): quantifier.to_name_structure() for (i, quantifier) in enumerate(generated_quantifiers)}
    json.dump({'quantifiers': gq_dict}, file, indent=2)

with open('results/generated_meanings.pickle', 'wb') as file:
    pickle.dump(list(expressions_by_meaning[bool].keys()), file)

with open('./results/generated_quantifiers.txt', 'w') as f:
    for quantifier in generated_quantifiers:
        f.write("{0}\n".format(quantifier))

print('Generation finished')
