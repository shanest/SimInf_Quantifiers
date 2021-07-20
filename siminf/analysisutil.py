import argparse
from siminf import experiment_setups 
from siminf import fileutil 
from siminf.fileutil import FileUtil 

def init(use_base_dir=False):
    
    parser = argparse.ArgumentParser(description="Analyze")
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--max_quantifier_length', type=int, required=True)
    parser.add_argument('--model_size', type=int, required=True)
    parser.add_argument('--dest_dir', default='results')
    parser.add_argument('--comp_strat', required=True)
    parser.add_argument('--inf_strat', required=True)
    parser.add_argument('--pareto', required=True)
    parser.add_argument('--table_name', required=True)
    parser.add_argument('--processes', default=4, type=int)
    parser.add_argument('--name', required=True)
    
    args = parser.parse_args()
    
    setup = experiment_setups.parse(args.setup)
    
    dirname = fileutil.base_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size) if use_base_dir \
        else fileutil.run_dir(args.dest_dir, setup.name, args.max_quantifier_length, args.model_size, args.name)
    file_util = FileUtil(dirname)
    return args, setup, file_util