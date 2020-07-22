import argparse
from pathos.pools import ProcessPool

from siminf.experiment_setups import ExperimentSetup 
from siminf import experiment_setups 

# # Parameters
from siminf import measurer 

from siminf import fileutil 
from siminf.fileutil import FileUtil 


def main():
    processes = args.processes
    setup = experiment_setups.parse(args.setup)
    max_quantifier_length = args.max_quantifier_length
    model_size = args.model_size

    file_util = FileUtil(fileutil.base_dir(args.dest_dir, setup.name, max_quantifier_length, model_size))

    folderName = "{0}/{1}_length={2}_size={3}".format(args.dest_dir, setup.name, max_quantifier_length, model_size)

    processpool = ProcessPool(nodes=processes)

    meanings = file_util.load_dill('meanings.dill')

    costs = processpool.map(measurer.measure_communicative_cost, meanings)

    file_util.dump_dill(costs, 'expression_costs.dill')

    processpool.close()
    processpool.join()

    print('Informativeness Measuring finished.')

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Measure expression informativeness")
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--max_quantifier_length', type=int, required=True)
    parser.add_argument('--model_size', type=int, required=True)
    parser.add_argument('--dest_dir', default='results')
    parser.add_argument('--processes', default=4, type=int)
    args = parser.parse_args()
    
    main()
