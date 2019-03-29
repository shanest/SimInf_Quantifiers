class WordCountComplexityMeasurer(object):

    def __init__(self, max_words):
        self.max_words = max_words

    def __call__(self, language):
        return len(language) / self.max_words