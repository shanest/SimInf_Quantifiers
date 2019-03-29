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