from itertools import product
from siminf import generator
import math


def flip_model(model):
    return generator.SimplifiedQuantifierModel(model.B, model.A, model.B - model.AandB, model.AandB)


class ConservativityMeasurer(object):

    def __init__(self, universe, model_size, conservative_set):
        self.universe = universe if conservative_set == 'A' else list(map(flip_model, universe))
        self.model_size = model_size

    def structure_meaning(self, raw_meaning):
        meaning = [[[None] * (self.model_size - B + 1) for AandB in range(B + 1)] for B in range(self.model_size + 1)]
        for j, model in enumerate(self.universe):
            meaning[model.B][model.AandB][model.AminusB] = raw_meaning[j]

        return meaning

    def create_conditional(self, raw_meaning):
        meaning = self.structure_meaning(raw_meaning)

        incidence = {(truth, subtruth): 0 for truth,subtruth in product([True,False],[True,False])}

        for B in range(self.model_size+1):
            for AandB in range(B+1):
                for AminusB in range(self.model_size-B+1):
                    truth = meaning[B][AandB][AminusB]
                    subtruth = meaning[B][AandB][0]
                    incidence[(truth, subtruth)] += 1

        probabilities = {}
        for (truth, subtruth) in product([True, False], [True, False]):
            probabilities[(truth, subtruth)] = incidence[(truth, subtruth)] / len(raw_meaning)

        return probabilities

    def __call__(self, meaning):
        probabilities = dict()
        probabilities[True] = sum(meaning)/len(meaning)
        probabilities[False] = 1-probabilities[True]

        conditional = self.create_conditional(meaning)
        probabilities_subtruth = dict()
        probabilities_subtruth[True] = conditional[(True, True)] + conditional[(False, True)]
        probabilities_subtruth[False] = 1-probabilities_subtruth[True]

        def entropy_helper(c, p):
            if p == 0 or c == 0:
                return 0
            return c * math.log(c/p)
        entropy_conditional = -sum(entropy_helper(conditional[(truth, subtruth)], probabilities_subtruth[subtruth])
                 for (truth, subtruth) in product([True, False],[True, False]))

        entropy_prior = -sum(probabilities[truth] * math.log(probabilities[truth]) for truth in [True,False] if
                             probabilities[truth] > 0)

        return max(0, min(1, 1 - entropy_conditional / entropy_prior if entropy_prior != 0 else 0))

