import analysisutil
import plotnine as pn
from Languages import LanguageLoader

analysisutil.add_argument('complexity_strategy')
analysisutil.add_argument('informativeness_strategy')
analysisutil.add_argument('--include_natural', dest='include_natural_languages', default=False, action='store_true')

(args, setup, file_util) = analysisutil.init()

data = LanguageLoader.load_pandas_table(file_util, args.complexity_strategy, args.informativeness_strategy)

fig = pn.ggplot(data, pn.aes('comm_cost', 'complexity')) +\
        pn.geom_point()

#if args.include_natural_languages:
 #   lex_informativeness = [inf for (ex,inf) in file_util.load_dill('informativeness_{0}_{1}.dill'.format(setup.name, args.informativeness_strategy))]
  #  lex_complexity = [com for (ex,com) in file_util.load_dill('complexity_{0}_{1}.dill'.format(setup.name, args.complexity_strategy))]
   # plt.plot(lex_informativeness, lex_complexity, 'o', color='green')

print(fig)

file_util.save_plotnine(fig, '{0}_{1}_plot'.format(
    args.complexity_strategy,
    args.informativeness_strategy
))