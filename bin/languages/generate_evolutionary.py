import argparse
import itertools
import math
import random
from copy import copy
import pygmo
from pathos.multiprocessing import ProcessPool
from siminf import generator 
from siminf import analysisutil
from siminf import experiment_setups 
from siminf import fileutil 
from siminf.fileutil import FileUtil 
from siminf.languages import language_loader, language_generator
from siminf.languages.complexity_measurer import SumComplexityMeasurer
from siminf.languages.informativeness_measurer import SimMaxInformativenessMeasurer

def remove(language, expressions=None):
    # the expressions argument is added so that the function
    # has the same signature as that of function add and interchange
    language = copy(language)
    index = random.randint(0,len(language)-1)
    language.pop(index)
    return language

def add(language, expressions):
    language = copy(language)
    while True:
        new_expression = random.choice(expressions)
        if new_expression not in language:
            language.append(new_expression)
            break
    return language

def interchange(language, expressions):
    return add(remove(language), expressions)

def mutate(language, expressions):
    possible_mutations = [interchange]
    if len(language) < args.lang_size:
        possible_mutations.append(add)
    if len(language) > 1:
        possible_mutations.append(remove)
    # calls a randomly selected function from remove, add, and interchange    
    mutation = random.choice(possible_mutations)
    return mutation(language, expressions)

def sample_mutated(languages, amount, expressions):
    amount -= len(languages)
    amount_per_language = int(math.floor(amount / len(languages)))
    amount_random = amount % len(languages)

    mutated_languages = []

    for language in languages:
        for i in range(amount_per_language):
            num_mutations = random.randint(1, args.max_mutations)
            mutated_language = language
            for j in range(num_mutations):
                mutated_language = mutate(mutated_language, expressions)
            mutated_languages.append(mutated_language)

    for i in range(amount_random):
        language = random.choice(languages)
        mutated_languages.append(mutate(language, expressions))

    mutated_languages.extend(languages)

    return mutated_languages


def main(args):    
    setup = experiment_setups.parse(args.setup)
    # use_base_dir = False
    dirname = fileutil.run_dir(setup.dest_dir, setup.name, setup.max_quantifier_length, setup.model_size, setup.pareto_name)
    file_util = FileUtil(dirname)
    
    expressions = language_loader.load_all_evaluated_expressions(file_util)
    languages_0 = language_generator.generate_sampled(expressions, args.lang_size, int(args.sample_size/args.lang_size))
    universe = generator.generate_simplified_models(setup.model_size)

    measure_complexity = SumComplexityMeasurer(args.lang_size, 1)
    measure_informativeness = SimMaxInformativenessMeasurer(universe)
    pool = ProcessPool(nodes=setup.processes)
    languages = languages_0    #lanuages will be iteratively updated in subsequent loop
    
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
        languages = sample_mutated(dominating_languages, args.sample_size, expressions)
    
    language_indices = [[e.index for e in lang] for lang in dominating_languages]
    dominating_complexity = [complexity[i] for i in dominating_indices]
    dominating_informativeness = [informativeness[i] for i in dominating_indices]
    
    file_util.dump_dill(dominating_complexity, 'complexity_wordcomplexity.dill')
    file_util.dump_dill(dominating_informativeness, 'informativeness_simmax.dill')
    file_util.dump_dill(language_indices, 'language_indices.dill')
    file_util.save_stringlist([list(map(str, lang)) for lang in languages], 'languages.txt')
    
    print("generate_evolutionary.py finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze")
    #common arguments
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    #additional arguments
    parser.add_argument('--lang_size', type=int, required=True)
    parser.add_argument('--sample_size', type=int, required=True)
    parser.add_argument('--generations', type=int, required=True)
    parser.add_argument('--max_mutations', type=int, default=1)
    #parse
    args = parser.parse_args()
    
    main(args)
