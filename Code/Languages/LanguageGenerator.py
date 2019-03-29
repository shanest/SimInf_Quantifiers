import itertools
import math
import random
from collections import namedtuple


EvaluatedExpression = namedtuple('EvaluatedExpression', 'expression meaning')


def generate_all(expressions, max_words):
    iterators = (itertools.combinations(expressions, word_amount) for word_amount in range(1, max_words+1))
    return list(itertools.chain(*iterators))


def generate_sampled(expressions, max_words, fraction):
    total_word_amount = len(expressions)
    languages = []

    for word_amount in range(1, max_words+1):
        num_samples = math.ceil(num_combinations(total_word_amount, word_amount) * fraction)
        if num_samples > 0:
            languages.extend(random_combinations(expressions, word_amount, num_samples))

    return languages


def random_combinations(iterable, r, amount):
    indices_list = []
    pool = tuple(iterable)
    n = len(pool)

    for i in range(amount):
        while True:
            indices = sorted(random.sample(range(n), r))
            if indices not in indices_list:
                indices_list.append(indices)
                break

    return (list(pool[i] for i in indices) for indices in indices_list)


def num_combinations(n, r):
    f = math.factorial
    return f(n) // f(r) // f(n - r)