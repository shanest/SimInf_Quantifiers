import math

from Expression import Expression
from Languages.InformativenessMeasurer import measure_informativeness
from Languages.LanguageGenerator import EvaluatedExpression


def evaluate_language(meanings, universe_size, target_utility):
    expression = Expression('test_expression', lambda model: True)
    language = [EvaluatedExpression(expression, meaning) for meaning in meanings]

    assert math.isclose(measure_informativeness(language, universe_size), target_utility)


def test_simple_language_1():
    meaning_1 = (True,True,True,False)
    meaning_2 = (False,False,False,True)

    evaluate_language([meaning_1,meaning_2], 4, .5)


def test_simple_language_2():
    meaning_1 = (True, False, False, False)
    meaning_2 = (False, True, False, False)
    meaning_3 = (False, False, True, False)
    meaning_4 = (False, False, False, True)

    evaluate_language([meaning_1, meaning_2, meaning_3, meaning_4], 4, 1)


def test_simple_language_3():
    meaning_1 = (True, False, False, False)
    meaning_2 = (False, True, False, False)
    meaning_3 = (False, False, True, False)
    meaning_4 = (False, True, False, True)

    evaluate_language([meaning_1, meaning_2, meaning_3, meaning_4], 4, 13/16)