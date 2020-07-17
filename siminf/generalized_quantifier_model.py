from collections import namedtuple
from siminf import set_place_holders as sph

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
    sph.A:                  lambda model: model.A,  
    sph.B:                  lambda model: model.B,
    sph.AminusB:            lambda model: model.AminusB,
    sph.AandB:              lambda model: model.AandB,
    sph.BminusA:            lambda model: model.B - model.AandB,
    sph.AunionB:            lambda model: model.B + model.AminusB,
    sph.AunionBminusAandB:  lambda model: model.B + model.AminusB - model.AandB,
    sph.empty:              lambda model: 0
}


def get_cardinality(model, set_placeholder):
    return cardinality_function[set_placeholder](model)


def subset(model, X, Y):
    for p in sph.representation[sph.minus(X, Y)]:
        if get_cardinality(model, p) > 0:
            return False
    return True