import itertools
import math
import random
from copy import copy

import pygmo
from pathos.multiprocessing import ProcessPool

import Generator
import analysisutil
from Languages import LanguageLoader, LanguageGenerator
from Languages.ComplexityMeasurer import SumComplexityMeasurer
from Languages.InformativenessMeasurer import SimMaxInformativenessMeasurer

analysisutil.add_argument('lang_size', type=int)
analysisutil.add_argument('sample_size', type=int)
analysisutil.add_argument('generations', type=int)
analysisutil.add_argument('-m','--max_mutations', type=int, default=1)
(args, setup, file_util) = analysisutil.init()

expressions = LanguageLoader.load_all_evaluated_expressions(file_util)

languages = LanguageGenerator.generate_sampled(expressions, args.lang_size, int(args.sample_size/args.lang_size))

universe = Generator.generate_simplified_models(args.model_size)


def remove(language):
    language = copy(language)
    index = random.randint(0,len(language)-1)
    language.pop(index)
    return language

def add(language):
    language = copy(language)
    while True:
        new_expression = random.choice(expressions)
        if new_expression not in language:
            language.append(new_expression)
            break
    return language

def interchange(language):
    return add(remove(language))

def mutate(language):
    possible_mutations = [interchange]
    if len(language) < args.lang_size:
        possible_mutations.append(add)
    if len(language) > 1:
        possible_mutations.append(remove)

    mutation = random.choice(possible_mutations)
    return mutation(language)


def sample_mutated(languages, amount):
    amount -= len(languages)
    amount_per_language = int(math.floor(amount / len(languages)))
    amount_random = amount % len(languages)

    mutated_languages = []

    for language in languages:
        for i in range(amount_per_language):
            num_mutations = random.randint(1, args.max_mutations)
            mutated_language = language
            for j in range(num_mutations):
                mutated_language = mutate(mutated_language)
            mutated_languages.append(mutate(language))

    for i in range(amount_random):
        language = random.choice(languages)
        mutated_languages.append(mutate(language))

    mutated_languages.extend(languages)

    return mutated_languages


measure_complexity = SumComplexityMeasurer(args.lang_size,1)
measure_informativeness = SimMaxInformativenessMeasurer(universe)
pool = ProcessPool(nodes=args.processes)

for gen in range(args.generations):
    print('GENERATION {0}'.format(gen))
    print('measuring')
    complexity = pool.map(measure_complexity, languages)
    informativeness = pool.map(measure_informativeness, languages)

    measurements = [(1 - inf, comp) for inf, comp in zip(informativeness, complexity)]

    print('calculating dominating')
    dominating_indices = pygmo.non_dominated_front_2d(measurements)
    dominating_languages = [languages[i] for i in dominating_indices]

    print('mutating')
    languages = sample_mutated(dominating_languages, args.sample_size)

language_indices = [[e.index for e in lang] for lang in dominating_languages]
dominating_complexity = [complexity[i] for i in dominating_indices]
dominating_informativeness = [informativeness[i] for i in dominating_indices]

file_util.dump_dill(dominating_complexity, 'complexity_wordcomplexity.dill')
file_util.dump_dill(dominating_informativeness, 'informativeness_simmax.dill')
file_util.dump_dill(language_indices, 'language_indices.dill')
file_util.save_stringlist([list(map(str, lang)) for lang in languages], 'languages.txt')
