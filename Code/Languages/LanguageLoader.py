from Languages.LanguageGenerator import EvaluatedExpression
import pandas as pd


def load_languages(file_util):
    file_util_base = file_util.get_base_file_util()
    unevaluated_expressions = file_util_base.load_dill('expressions.dill')
    meanings = file_util_base.load_dill('meanings.dill')
    complexities = file_util_base.load_dill('expression_complexities.dill')
    monotonicities = file_util_base.load_dill('monotonicities_max.dill')
    conservativities = file_util_base.load_dill('conservativities_max.dill')
    special_complexities = file_util_base.load_dill('expression_special_complexities.dill')

    index_lists = file_util.load_dill('language_indices.dill')

    languages = []
    for indices in index_lists:
        languages.append([EvaluatedExpression(unevaluated_expressions[i], meanings[i], complexities[i],
                                              monotonicities[i], conservativities[i], special_complexities[i], i)
                          for i in indices])

    return languages


def load_all_evaluated_expressions(file_util):
    file_util_base = file_util.get_base_file_util()
    unevaluated_expressions = file_util_base.load_dill('expressions.dill')
    meanings = file_util_base.load_dill('meanings.dill')
    complexities = file_util_base.load_dill('expression_complexities.dill')
    monotonicities = file_util_base.load_dill('monotonicities_max.dill')
    conservativities = file_util_base.load_dill('conservativities_max.dill')
    special_complexities = file_util_base.load_dill('expression_special_complexities.dill')

    return [EvaluatedExpression(unevaluated_expressions[i], meanings[i], complexities[i], monotonicities[i],
                                conservativities[i], special_complexities[i], i)
            for i in range(len(unevaluated_expressions))]


def load_pandas_table(file_util, complexity_strategy, informativeness_strategy, include_monotonicity=True):
    complexity = file_util.load_dill('complexity_{0}.dill'.format(complexity_strategy))
    informativeness = file_util.load_dill('informativeness_{0}.dill'.format(informativeness_strategy))

    data = {'complexity': complexity,
            'comm_cost': list(map(lambda x: 1 - x, informativeness))
           }
    if include_monotonicity:
        data['monotonicity'] = file_util.load_dill('monotonicity.dill')

    return pd.DataFrame(data)

