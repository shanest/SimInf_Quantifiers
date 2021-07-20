from pathos.multiprocessing import ProcessPool

from siminf import generator
from siminf import analysisutil
from siminf.conservativity import ConservativityMeasurer

def main():

    (args, setup, file_util) = analysisutil.init(use_base_dir=True)

    meanings = file_util.load_dill('meanings.dill')

    universe = generator.generate_simplified_models(setup.model_size)

    measurer_a = ConservativityMeasurer(universe,setup.model_size,'A')
    measurer_b = ConservativityMeasurer(universe,setup.model_size,'B')

    with ProcessPool(nodes=setup.processes) as process_pool:
        conservativities_a = process_pool.map(measurer_a, meanings)
        conservativities_b = process_pool.map(measurer_b, meanings)
        conservativities_max = process_pool.map(max, conservativities_a, conservativities_b)

    file_util.dump_dill(conservativities_a, 'conservativities_a.dill')
    file_util.dump_dill(conservativities_b, 'conservativities_b.dill')
    file_util.dump_dill(conservativities_max, 'conservativities_max.dill')
    
    print("measure_expression_conservativity.py finished.")


if __name__ == "__main__":
    main()
