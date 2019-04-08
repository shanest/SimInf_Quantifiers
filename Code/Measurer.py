def measure_complexity(quantifier, max_length):
    return (measure_expression_complexity(quantifier.expression, max_length) +
            measure_expression_complexity(quantifier.presupposition, max_length)) / 2


def measure_expression_complexity(expression, max_length):
    return expression.length()/max_length if expression is not None else 0

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
    true_count = meaning.count(True)
    return true_count/len(meaning) if true_count > 0 else 1

def measure_relative_communicative_cost(meaning):
    true_count = meaning.count(True)
    false_count = meaning.count(False)
    return true_count / (true_count + false_count) if true_count > 0 else 1
