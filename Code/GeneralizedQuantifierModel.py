from collections import namedtuple

import SetPlaceholders


class GeneralizedQuantifierModel:

    def __init__(self, M, A, B):
        self.dictionary = {
            'M': M,
            'A': A,
            'B': B
        }

    def get_set(self, model_set_name):
        return self.dictionary[model_set_name]


SimplifiedQuantifierModel = namedtuple("SimplifiedQuantifierModel", "A B AminusB AandB")

cardinality_function = {
    SetPlaceholders.A: lambda model: model.A,
    SetPlaceholders.B: lambda model: model.B,
    SetPlaceholders.AminusB: lambda model: model.AminusB,
    SetPlaceholders.AandB: lambda model: model.AandB,
    SetPlaceholders.BminusA: lambda model: model.B - model.AandB,
    SetPlaceholders.AunionB: lambda model: model.B + model.AminusB,
    SetPlaceholders.AunionBminusAandB: lambda model: model.B + model.AminusB - model.AandB,
    SetPlaceholders.empty: lambda model: 0
}


def get_cardinality(model, set_placeholder):
    return cardinality_function[set_placeholder](model)


def subset(model, X, Y):
    for placeholder in SetPlaceholders.representation[SetPlaceholders.minus(X, Y)]:
        if get_cardinality(model, placeholder) > 0:
            return False
    return True