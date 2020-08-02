import argparse
import os
import dill

from siminf import parser as simparser
from siminf.experiment_setups import ExperimentSetup 
from siminf import experiment_setups 

from siminf.generator import MeaningCalculator # replacing from Generator import MeaningCalculator

def main(args):

    setup = experiment_setups.parse(args.setup)
    universe = setup.generate_models(args.model_size)

    quantifiers = simparser.load_from_file(setup.lexical_quantifiers_filename, setup) #not to be confused with Argument parser

    calculate_meaning = MeaningCalculator(universe)

    meanings = {name: calculate_meaning(quantifier) for (name, quantifier) in quantifiers.items()}

    file_dir = '{0}/lexicalized_meanings'.format(args.dest_dir)
    file_name = '{0}_size={1}.dill'.format(setup.name, args.model_size)
    
    print("file_dir={0}".format(file_dir))
    print("file_name={0}".format(file_name))
    
    os.makedirs(file_dir, exist_ok=True)   
    with open('{0}/{1}'.format(file_dir, file_name), 'wb') as file:
        dill.dump(meanings, file)
        
    print("calculate_meanings finished.")
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Calculate the meanings of the lexicalized quantifiers")
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    parser.add_argument('--model_size', type=int, required=True)
    parser.add_argument('--dest_dir', default='results')
    args = parser.parse_args()
    
    main(args)
