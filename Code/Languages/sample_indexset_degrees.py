import random

import analysisutil
from Languages.LanguageGenerator import random_combinations

analysisutil.add_argument('indices')
analysisutil.add_argument('max_words', type=int)
analysisutil.add_argument('sample', type=int)
(args, setup, file_util_out) = analysisutil.init()
file_util_in = file_util_out.get_base_file_util()

natural_indices = set(file_util_in.load_dill('{0}_expression_indices.dill'.format(args.indices)))
expressions = file_util_in.load_dill('expressions.dill')
non_natural_indices = set(range(len(expressions))) - natural_indices

language_indices = []
naturalness = []
sizes = []

for lang_size in range(1,args.max_words+1):
    for i in range(args.sample):
        len_natural = random.randint(0,lang_size)
        len_random = lang_size - len_natural
        lang_random = next(random_combinations(non_natural_indices, len_random, 1))
        lang_natural = next(random_combinations(natural_indices, len_natural, 1))
        naturalness.append(len_natural / lang_size)
        language_indices.append(lang_random + lang_natural)

file_util_out.dump_dill(language_indices, 'language_indices.dill')
file_util_out.dump_dill(naturalness, 'naturalness.dill')
file_util_out.save_stringlist([list(map(lambda i: str(expressions[i]), lang)) for lang in language_indices], 'languages.txt')
