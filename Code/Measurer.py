import numpy

from SetPlaceholders import SetPlaceholder


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


class SpecialComplexityMeasurer(object):

    def __init__(self, operators, model_size):
        self.operators = operators

        type_options = [SetPlaceholder, int, float, bool]
        type_count = {_type: 0 for _type in type_options}
        for operator in operators.values():
            type_count[operator.outputType] += 1

        type_count[SetPlaceholder] += 2  # A and B
        type_count[int] += len(range(0, model_size + 1, 2))
        type_count[float] += 10

        self.type_probabilities = {}
        for _type in type_options:
            self.type_probabilities[_type] = 1 / type_count[_type]

    def measure_expression_probability(self, expression):
        if expression.name == 'A' or expression.name == 'B':
            primitive = True
            _type = SetPlaceholder
        elif not isinstance(expression.name, str):
            primitive = True
            _type = float if type(expression.name) == numpy.float64 else type(expression.name)
        else:
            primitive = False
            _type = self.operators[expression.name].outputType

        self_probability = self.type_probabilities[_type]
        args_probability = 1 if primitive else \
            numpy.prod([self.measure_expression_probability(arg) for arg in expression.arg_expressions])

        return self_probability * args_probability

    def __call__(self,expression):
        probability = self.measure_expression_probability(expression)
        return 1 - 1 / (1 + numpy.exp(2*probability))