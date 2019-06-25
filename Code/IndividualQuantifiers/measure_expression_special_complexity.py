import numpy

import numpy as np
from pathos.multiprocessing import ProcessPool

import Generator
import analysisutil
from Measurer import SpecialComplexityMeasurer
from Monotonicity import MonotonicityMeasurer
from SetPlaceholders import SetPlaceholder

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

operators = setup.operators


expressions = file_util.load_dill('expressions.dill')

measurer = SpecialComplexityMeasurer(operators, args.model_size)

with ProcessPool(nodes=args.processes) as process_pool:
    special_complexities = process_pool.map(measurer, expressions)

file_util.dump_dill(special_complexities, 'expression_special_complexities.dill')
