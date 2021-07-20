import argparse
from pathos.pools import ProcessPool
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
    
    folderName = "{0}/{1}_length={2}_size={3}".format(setup.dest_dir, setup.name, max_quantifier_length, model_size)
    
    processpool = ProcessPool(nodes=processes)
    
    expressions = file_util.load_dill('expressions.dill')
    
    complexities = processpool.map(lambda ex: setup.measure_expression_complexity(ex, max_quantifier_length), expressions)
    
    file_util.dump_dill(complexities, 'expression_complexities.dill')
    
    processpool.close()
    processpool.join()
    
    print('Complexity Measuring finished.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Quantifiers")
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    args = parser.parse_args()
    
    main(args)
