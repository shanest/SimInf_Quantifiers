import pygmo

import analysisutil
import matplotlib.pyplot as plt

analysisutil.add_argument('complexity_strategy')
analysisutil.add_argument('informativeness_strategy')
analysisutil.add_argument('--include_natural', dest='include_natural_languages', default=False, action='store_true')

(args, setup, file_util) = analysisutil.init()

informativeness = file_util.load_dill('informativeness_{0}.dill'.format(args.informativeness_strategy))
complexity = file_util.load_dill('complexity_{0}.dill'.format(args.complexity_strategy))

measurements = [(1-inf, comp) for inf, comp in zip(informativeness, complexity)]

dominating_indices = pygmo.non_dominated_front_2d(measurements)

dom_informativeness = [informativeness[i] for i in dominating_indices]
dom_complexity = [complexity[i] for i in dominating_indices]

fig = plt.figure()
plt.plot(informativeness,complexity,'o')
plt.plot(dom_informativeness,dom_complexity,'o',color='red')
#plt.axis([0,1,0,1])

if args.include_natural_languages:
    lex_informativeness = [inf for (ex,inf) in file_util.load_dill('informativeness_{0}_{1}.dill'.format(setup.name, args.informativeness_strategy))]
    lex_complexity = [com for (ex,com) in file_util.load_dill('complexity_{0}_{1}.dill'.format(setup.name, args.complexity_strategy))]
    plt.plot(lex_informativeness, lex_complexity, 'o', color='green')

plt.xlabel('informativeness')
plt.ylabel('complexity')

plt.show()

file_util.save_figure(fig, '{0}_{1}_plot'.format(
    args.complexity_strategy,
    args.informativeness_strategy
))