import random
from collections import namedtuple

from pathos.multiprocessing import ProcessPool

import Generator
import analysisutil
from Languages.ComplexityMeasurer import WordCountComplexityMeasurer
from Languages.InformativenessMeasurer import InformativenessMeasurer, SimMaxInformativenessMeasurer
from Languages.LanguageGenerator import generate_all, generate_sampled, EvaluatedExpression

analysisutil.add_argument('max_words', type=int)
analysisutil.add_argument('--sample', type=int)
(args, setup, file_util) = analysisutil.init()

languages = []

universe = Generator.generate_simplified_models(args.model_size)

FakeEvaluatedExpression = namedtuple('FakeEvaluatedExpression', 'meaning')

expressions = [FakeEvaluatedExpression(tuple([random.choice([True, False]) for model in universe]))
               for i in range(10000)]

if args.sample is None:
    languages = generate_all(expressions, args.max_words, args.fixedwordcount)
else:
    languages = generate_sampled(expressions, args.max_words, args.sample)

complexity_measurer = WordCountComplexityMeasurer(args.max_words)
informativeness_measurer_exact = InformativenessMeasurer(len(universe))
informativeness_measurer_simmax = SimMaxInformativenessMeasurer(universe)

with ProcessPool(nodes=args.processes) as pool:
    complexity = pool.map(complexity_measurer, languages)
    informativeness_exact = pool.map(informativeness_measurer_exact, languages)
    informativeness_simmax = pool.map(informativeness_measurer_simmax, languages)

file_util.dump_dill(complexity, 'complexity_wordcount.dill')
file_util.dump_dill(informativeness_exact, 'informativeness_exact.dill')
file_util.dump_dill(informativeness_simmax, 'informativeness_simmax.dill')

