class WordCountComplexityMeasurer(object):

    def __init__(self, max_words):
        self.max_words = max_words

    def __call__(self, language):
        return len(language) / self.max_words


class SumComplexityMeasurer(object):

    def __init__(self, max_words, max_word_complexity):
        self.max_complexity = max_words*max_word_complexity

    def __call__(self, language):
        return sum(word.complexity for word in language) / self.max_complexity


class SpecialComplexityMeasurer(object):

    def __init__(self, max_words):
        self.max_complexity = max_words

    def __call__(self, language):
        return sum(word.special_complexity for word in language) / self.max_complexity
