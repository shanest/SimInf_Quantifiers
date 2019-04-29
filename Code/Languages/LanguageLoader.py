from Languages.LanguageGenerator import EvaluatedExpression


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
                                              monotonicities[i], conservativities[i], special_complexities[i])
                          for i in indices])

    return languages