import argparse
import random
from collections import namedtuple
from pathos.multiprocessing import ProcessPool

from siminf import experiment_setups2
from siminf import generator
from siminf.languages.complexity_measurer import WordCountComplexityMeasurer
from siminf.languages.informativeness_measurer import InformativenessMeasurer, SimMaxInformativenessMeasurer
from siminf.languages.language_generator import generate_all, generate_sampled, EvaluatedExpression

def main(args):   
    setup = experiment_setups2.parse(args.setup)
    setup.show_loaded_setups()
    setup.show_parsed_setups()
    
    languages = []
    universe = generator.generate_simplified_models(setup.model_size)

    FakeEvaluatedExpression = namedtuple('FakeEvaluatedExpression', 'meaning')    
    expressions = [FakeEvaluatedExpression(tuple([random.choice([True, False]) for model in universe]))
                    for i in range(int(setup['random_size']))]

    if setup['sample'] is None:
        print("generate_all() called.")
        languages = generate_all(expressions, int(setup['max_words']), int(setup['fixedwordcount']))
    else:
        print("generate_sampled() called.")
        languages = generate_sampled(expressions, int(setup['max_words']), int(setup['sample']))

    complexity_measurer = WordCountComplexityMeasurer(int(setup['max_words']))
    informativeness_measurer_exact = InformativenessMeasurer(len(universe))
    informativeness_measurer_simmax = SimMaxInformativenessMeasurer(universe)

    with ProcessPool(nodes=setup.processes) as pool:
        complexity = pool.map(complexity_measurer, languages)
        informativeness_exact = pool.map(informativeness_measurer_exact, languages)
        informativeness_simmax = pool.map(informativeness_measurer_simmax, languages)
        
    file_util = setup.file_util
    file_util.dump_dill(complexity, 'complexity_wordcount2.dill')
    file_util.dump_dill(informativeness_exact, 'informativeness_exact2.dill')
    file_util.dump_dill(informativeness_simmax, 'informativeness_simmax2.dill')
    
    print("coinflip_languages.py finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze")
    parser.add_argument('--setup', help='Path to the setup json file.', required=True)
    args = parser.parse_args()
    main(args)
