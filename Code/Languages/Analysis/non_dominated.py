from collections import namedtuple

import pygmo

from analysisutil import file_util, args

languages = file_util.load_dill('languages.dill')
informativeness = file_util.load_dill('informativeness_{0}.dill'.format(args.informativeness_strategy))
complexity = file_util.load_dill('complexity_{0}.dill'.format(args.complexity_strategy))

measurements = [(inf, 1-comp) for inf, comp in zip(informativeness, complexity)]

dominating_indices = pygmo.non_dominated_front_2d(measurements)

dominating_languages = [languages[index] for index in dominating_indices]

with open('{0}/dominating_languages.txt'.format(file_util.folderName), 'w') as f:
    for language in dominating_languages:
        f.write("{0}\n".format([str(e.expression) for e in language]))