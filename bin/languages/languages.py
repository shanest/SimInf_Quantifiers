import argparse
from siminf import experiment_setups
from siminf import fileutil
from siminf.languages.language_generator import EvaluatedExpression, generate_all, generate_sampled
from siminf.fileutil import FileUtil

def main(args):    
    setup = experiment_setups.parse(args.setup)
    
    file_util_out = FileUtil(fileutil.run_dir(setup.dest_dir, setup.name, setup.max_quantifier_length, setup.model_size, setup.random_name))
    file_util_in = FileUtil(fileutil.base_dir(setup.dest_dir, setup.name, setup.max_quantifier_length, setup.model_size))
    
    unevaluated_expressions = file_util_in.load_dill('expressions.dill')
    
    if args.indices is not None:
        index_sets = []
        for indices_name in args.indices:
            index_sets.append(set(file_util_in.load_dill('{0}_expression_indices.dill'.format(indices_name))))
        indices = set.intersection(*index_sets)
    else:
        indices = range(len(unevaluated_expressions))
    
    if args.sample is None:
        languages = generate_all(indices, args.max_words, args.fixedwordcount)
    else:
        languages = generate_sampled(indices, setup.max_words, args.sample)
    
    file_util_out.dump_dill(languages, 'language_indices.dill')
    file_util_out.save_stringlist([list(map(str, lang)) for lang in languages], 'languages.txt')
    
    print("languages.py finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Quantifiers")
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--sample', type=int, default=None)
    parser.add_argument('-i','--indices', nargs='*')
    args = parser.parse_args()    
    
    main(args)