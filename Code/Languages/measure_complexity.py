from pathos.pools import ProcessPool
import analysisutil
from Languages import LanguageLoader
from Languages.ComplexityMeasurer import WordCountComplexityMeasurer, SumComplexityMeasurer, SpecialComplexityMeasurer

(args, setup, file_util) = analysisutil.init()
analysisutil.add_argument('max_words')
analysisutil.add_argument('comp_strat')

languages = LanguageLoader.load_languages(file_util)

if args.comp_strat == 'wordcount':
    complexity_measurer = WordCountComplexityMeasurer(args.max_words)
elif args.comp_strat == 'wordcomplexity':
    complexity_measurer = SumComplexityMeasurer(args.max_words, 1)
elif args.comp_strat == 'special':
    complexity_measurer = SpecialComplexityMeasurer(args.max_words)
else:
    raise ValueError('{0} is not a valid complexity strategy.'.format(args.comp_strat))

with ProcessPool(nodes=args.processes) as pool:
    complexity = pool.map(complexity_measurer, languages)

file_util.dump_dill(complexity, 'complexity_{0}.dill'.format(args.comp_strat))

