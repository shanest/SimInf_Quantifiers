from itertools import product
import Generator
import math


def flip_model(model):
    return Generator.SimplifiedQuantifierModel(model.B, model.A, model.B - model.AandB, model.AandB)


class MonotonicityMeasurer(object):

    def __init__(self, universe, model_size, monotone_set, down=False):
        self.universe = universe if monotone_set == 'A' else list(map(flip_model, universe))
        self.model_size = model_size
        self.create_conditional = self.create_conditional_downward if down else self.create_conditional_upward

    def structure_meaning(self, raw_meaning):
        meaning = [[[None] * (self.model_size - B + 1) for AandB in range(B + 1)] for B in range(self.model_size + 1)]
        for j, model in enumerate(self.universe):
            meaning[model.B][model.AandB][model.AminusB] = raw_meaning[j]

        return meaning

    def create_conditional_upward(self, raw_meaning):
        meaning = self.structure_meaning(raw_meaning)

        truth_below = [[[None] * (self.model_size - B + 1) for AandB in range(B + 1)] for B in range(self.model_size + 1)]
        incidence = {(truth, subtruth): 0 for (truth, subtruth) in product([True, False],[True, False])}

        # Build up submodel truth
        for B in range(self.model_size+1):
            truth_below[B][0][0] = meaning[B][0][0]
            for AandB in range(1,B+1):
                truth_below[B][AandB][0] = truth_below[B][AandB-1][0] or meaning[B][AandB][0]
            for AminusB in range(1,self.model_size-B+1):
                truth_below[B][0][AminusB] = truth_below[B][0][AminusB-1] or meaning[B][0][AminusB]

            for AandB in range(1,B+1):
                for AminusB in range(1,self.model_size-B+1):
                    truth_below[B][AandB][AminusB] = \
                        truth_below[B][AandB-1][AminusB] or \
                        truth_below[B][AandB][AminusB-1] or \
                        meaning[B][AandB][AminusB]

        for B in range(self.model_size+1):
            for AandB in range(B+1):
                for AminusB in range(self.model_size-B+1):
                    incidence[(meaning[B][AandB][AminusB], truth_below[B][AandB][AminusB])] += 1

        probabilities = {}
        for (truth, subtruth) in product([True, False],[True, False]):
            probabilities[(truth, subtruth)] = incidence[(truth, subtruth)] / len(raw_meaning)

        return probabilities

    def create_conditional_downward(self, raw_meaning):
        meaning = self.structure_meaning(raw_meaning)

        truth_above = [[[None] * (self.model_size - B + 1) for AandB in range(B + 1)] for B in range(self.model_size + 1)]
        incidence = {(truth, subtruth): 0 for (truth, subtruth) in product([True, False],[True, False])}

        # Build up supermodel truth
        def calculate_truth_above(B,AandB,AminusB):
            if truth_above[B][AandB][AminusB] is None:
                result = meaning[B][AandB][AminusB]
                if AandB < B:
                    result = calculate_truth_above(B,AandB+1,AminusB) or result
                if AminusB + B < self.model_size:
                    result = calculate_truth_above(B, AandB, AminusB+1) or result
                truth_above[B][AandB][AminusB] = result

            return truth_above[B][AandB][AminusB]

        for B in range(self.model_size+1):
            calculate_truth_above(B,0,0)
            for AandB in range(B+1):
                for AminusB in range(self.model_size-B+1):
                    incidence[(meaning[B][AandB][AminusB], truth_above[B][AandB][AminusB])] += 1

        probabilities = {}
        for (truth, subtruth) in product([True, False],[True, False]):
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

