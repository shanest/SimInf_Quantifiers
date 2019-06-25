import pygmo
import analysisutil

analysisutil.add_argument('complexity_strategy')
analysisutil.add_argument('informativeness_strategy')

(args, setup, file_util) = analysisutil.init()

languages = file_util.load_dill('languages.dill')
informativeness = file_util.load_dill('informativeness_{0}.dill'.format(args.informativeness_strategy))
complexity = file_util.load_dill('complexity_{0}.dill'.format(args.complexity_strategy))

measurements = [(1-inf, comp) for inf, comp in zip(informativeness, complexity)]

dominating_indices = pygmo.non_dominated_front_2d(measurements)

dominating_languages = [(languages[i], complexity[i], informativeness[i]) for i in dominating_indices]

filename = '{0}/dominating_languages_{1}_{2}.txt'.format(
    file_util.folderName,
    args.complexity_strategy,
    args.informativeness_strategy
)

with open(filename, 'w') as f:
    for lang, comp, inf in dominating_languages:
        f.write("{0}\nComplexity      : {1}\nInformativeness : {2}\n".format(list(map(str, lang)), comp, inf))