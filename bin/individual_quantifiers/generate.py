import argparse
import os

from pathos.pools import ProcessPool

from siminf.generator import ExpressionGenerator
from siminf.experiment_setups import ExperimentSetup 
from siminf import experiment_setups 

# Parameters
from siminf import fileutil
from siminf.fileutil import FileUtil

def main(args):

    setup = experiment_setups.parse(args.setup)
    processes = setup.processes
    max_quantifier_length = setup.max_quantifier_length
    model_size = setup.model_size
    
    file_util = FileUtil(fileutil.base_dir(setup.dest_dir, setup.name, max_quantifier_length, model_size))
    
    universe = setup.generate_models(model_size)
    
    folderName = "{0}/{1}_length={2}_size={3}".format(setup.dest_dir,setup.name,max_quantifier_length,model_size)
    os.makedirs("{0}".format(folderName), exist_ok=True)
    
    processpool = ProcessPool(nodes=processes)
    expression_generator = ExpressionGenerator(setup, model_size, universe, processpool)
    (generated_expressions_dict, expressions_by_meaning) = \
          expression_generator.generate_all_expressions(max_quantifier_length)
    
    print("{0} expressions!".format(len(expressions_by_meaning[bool].values())))
    
    file_util.dump_dill(expressions_by_meaning[bool], 'generated_expressions.dill')
    file_util.dump_dill(list(expressions_by_meaning[bool].values()), 'expressions.dill')
    file_util.dump_dill(list(expressions_by_meaning[bool].keys()), 'meanings.dill')
    
    processpool.close()
    processpool.join()
    
    print('Expression generation finished.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Quantifiers")
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    args = parser.parse_args()
    
    main(args)
