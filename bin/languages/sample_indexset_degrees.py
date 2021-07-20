import argparse
import random
from siminf import analysisutil
from siminf import fileutil 
from siminf.fileutil import FileUtil 
from siminf import experiment_setups 
from siminf.languages.language_generator import random_combinations

def main(args): 
    setup = experiment_setups.parse(args.setup)
    dirname = fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name)
    file_util_out = FileUtil(dirname)
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
    
    print("sample_indexset_degrees.py finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze")
    #common arguments
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--max_quantifier_length', type=int, required=True)
    parser.add_argument('--model_size', type=int, required=True)
    parser.add_argument('--dest_dir', default='results')
    parser.add_argument('--processes', default=4, type=int)
    parser.add_argument('--name', default='run_0')
    #additional arguments    
    parser.add_argument('--indices', required=True)
    parser.add_argument('--max_words', type=int, required=True)
    parser.add_argument('--sample', type=int, required=True)
    #parse
    args = parser.parse_args()
    
    main(args)
