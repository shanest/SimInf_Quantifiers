import argparse
from siminf import experiment_setups 
from siminf import fileutil 
from siminf.fileutil import FileUtil 

def init(use_base_dir=False):
    
    parser = argparse.ArgumentParser(description="Analyze")
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    args = parser.parse_args()
    
    setup = experiment_setups.parse(args.setup)
    
    dirname = fileutil.base_dir(setup.dest_dir, setup.name, setup.max_quantifier_length, setup.model_size) if use_base_dir \
        else fileutil.run_dir(setup.dest_dir, setup.name, setup.max_quantifier_length, setup.model_size, setup.name)
    file_util = FileUtil(dirname)
    return args, setup, file_util