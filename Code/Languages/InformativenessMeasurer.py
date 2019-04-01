import itertools

from GeneralizedQuantifierModel import SimplifiedQuantifierModel


def measure_informativeness(language, universe_size):
    utility = 0

    for state in range(universe_size):
        words_for_state = set(filter(lambda word: word.meaning[state], language))
        word_amount = len(words_for_state)

        for word in words_for_state:
            word_meaning_size = sum(word.meaning)
            utility += 1 / universe_size / word_amount / word_meaning_size

    return utility


class InformativenessMeasurer(object):

    def __init__(self, universe_size):
        self.universe_size = universe_size

    def __call__(self, language):
        return measure_informativeness(language, self.universe_size)


def distance(s1: SimplifiedQuantifierModel, s2: SimplifiedQuantifierModel):
    AminusBdec = s1.AminusB - s2.AminusB
    AandBdec = s1.AandB - s2.AandB
    BminusAdec = s1.B - s1.AandB - (s2.B - s2.AandB)
    total_increase = (s2.AminusB + s2.B) - (s1.AminusB + s1.B)

    return sum(max(var, 0) for var in [AminusBdec, AandBdec, BminusAdec, total_increase])


class SimMaxInformativenessMeasurer(object):

    def __init__(self, universe, model_size):
        self.universe = universe
        self.score = {}
        for (i1,s1),(i2,s2) in itertools.combinations(enumerate(universe),2):
            dist = distance(s1,s2)
            self.score[(i1, i2)] = 1/(dist+1)
            self.score[(i2, i1)] = 1/(dist+1)
        for index in range(len(universe)):
            self.score[(index, index)] = 1

    def __call__(self, language):
        utility = 0

        for index in range(len(self.universe)):
            words_for_state = set(filter(lambda word: word.meaning[index], language))
            word_amount = len(words_for_state)

            for word in words_for_state:
                word_meaning_size = sum(word.meaning)
                for other_index, truth_value in enumerate(word.meaning):
                    if truth_value:
                        score = self.score[(index, other_index)]
                        utility += score / len(self.universe) / word_amount / word_meaning_size

        return utility