import numpy as np
from pathos.multiprocessing import ProcessPool

import Generator
import analysisutil
from Monotonicity import MonotonicityMeasurer
from SetPlaceholders import SetPlaceholder

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

operators = setup.operators
type_options = [SetPlaceholder, int, float, bool]
type_count = {_type: 0 for _type in type_options}
for _type in type_options:
    type_count[_type] += 1

type_count[SetPlaceholder] += 2 # A and B
type_count[int] += len(range(0, args.model_size+1, 2))
type_count[float] += 10

type_probabilities = {}
for _type in type_options:
    type_probabilities[_type] = 1 / type_count[_type]


def measure_expression_probability(expression):
    if expression.name == 'A' or expression.name == 'B':
        primitive = True
        _type = SetPlaceholder
    elif not isinstance(expression.name, str):
        primitive = True
        _type = type(expression.name)
    else:
        primitive = False
        _type = operators[expression.name].outputType

    self_probability = type_probabilities[_type]
    args_probability = 1 if primitive else \
        np.prod([measure_expression_probability(arg) for arg in expression.arg_expressions])

    return self_probability * args_probability

def measure_special_complexity(expression):
    probability = measure_expression_probability(expression)
    return - np.log(probability)

expressions = file_util.load_dill('expressions.dill')

with ProcessPool(nodes=args.processes) as process_pool:
    special_complexities = process_pool.map(measure_special_complexity, expressions)

file_util.dump_dill(special_complexities, 'expression_special_complexities.dill')
