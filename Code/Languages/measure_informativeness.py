from pathos.pools import ProcessPool
import Generator
import analysisutil
from Languages import LanguageLoader
from Languages.InformativenessMeasurer import SimMaxInformativenessMeasurer, InformativenessMeasurer

(args, setup, file_util) = analysisutil.init()
analysisutil.add_argument('inf_strat')

languages = LanguageLoader.load_languages(file_util)

universe = Generator.generate_simplified_models(args.model_size)

if args.inf_strat == 'exact':
    informativeness_measurer = InformativenessMeasurer(len(universe))
elif args.inf_strat == 'simmax':
    informativeness_measurer = SimMaxInformativenessMeasurer(universe)
else:
    raise ValueError('{0} is not a valid informativeness strategy.'.format(args.inf_strat))

with ProcessPool(nodes=args.processes) as pool:
    informativeness = pool.map(informativeness_measurer, languages)

file_util.dump_dill(informativeness, 'informativeness_{0}.dill'.format(args.inf_strat))

