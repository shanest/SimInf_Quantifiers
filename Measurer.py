import collections

def measure_complexity(quantifier):
    return measure_expression_complexity(quantifier.expression) + measure_expression_complexity(quantifier.presupposition)


def measure_expression_complexity(expression):
    return expression.length()/20 if expression is not None else 0


# def measure_relative_communicative_cost(quantifier, universe):
#     true_count = 0
#     total_count = 0
#     for model in universe:
#         truth_value = quantifier.evaluate(model)
#         if truth_value is not None:
#             total_count += 1
#             true_count += 1 if truth_value else 0
#
#     return true_count / total_count if true_count > 0 else 1
#
#
# def measure_communicative_cost(quantifier, universe):
#     true_count = 0
#     for model in universe:
#         if quantifier.evaluate(model) is True:
#             true_count += 1
#
#     return true_count / len(universe) if true_count > 0 else 1

def measure_communicative_cost(meaning):
    return meaning.count(True)/len(meaning)

def measure_relative_communicative_cost(meaning):
    true_count = meaning.count(True)
    false_count = meaning.count(False)
    return true_count / (true_count + false_count)
