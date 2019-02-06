class GeneralizedQuantifierModel:

    def __init__(self, M, A, B):
        self.dictionary = {
            'M': M,
            'A': A,
            'B': B
        }

    def get_set(self, model_set_name):
        return self.dictionary[model_set_name]
