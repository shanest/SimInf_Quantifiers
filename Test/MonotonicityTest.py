import math
import random

import Generator
import Parser
from Monotonicity import MonotonicityMeasurer


class Setup:
    parse_primitive = Parser.parse_simple_primitive_with_sets


def test_completely_upward_monotone():
    expression = Parser.parse_expression(['>',['card','A'],6],Setup)
    universe = Generator.generate_simplified_models(10)

    meaning = Generator.MeaningCalculator(universe)(expression)

    measurer = MonotonicityMeasurer(universe, 10, 'A')

    monotonicity = measurer(meaning)

    assert math.isclose(monotonicity, 1)


def test_completely_downward_monotone():
    expression = Parser.parse_expression(['>',6,['card','A']],Setup)
    universe = Generator.generate_simplified_models(10)

    meaning = Generator.MeaningCalculator(universe)(expression)

    measurer = MonotonicityMeasurer(universe, 10, 'A', down=True)

    monotonicity = measurer(meaning)

    assert math.isclose(monotonicity, 1)


def test_completely_upward_monotone_a():
    expression = Parser.parse_expression(['subset','B','A'],Setup)
    universe = Generator.generate_simplified_models(10)

    meaning = Generator.MeaningCalculator(universe)(expression)

    measurer = MonotonicityMeasurer(universe, 10, 'A')

    monotonicity = measurer(meaning)

    assert math.isclose(monotonicity, 1)

def test_not_upward_monotone_a():
    expression = Parser.parse_expression(['subset','A','B'],Setup)
    universe = Generator.generate_simplified_models(10)

    meaning = Generator.MeaningCalculator(universe)(expression)

    measurer = MonotonicityMeasurer(universe, 10, 'A')

    monotonicity = measurer(meaning)

    assert not math.isclose(monotonicity, 1)

def test_not_entirely_upward_monotone_a():
    expression = Parser.parse_expression(['and',['>',['card',['intersection','A','B']],3],['>',9,['card',['intersection','A','B']]]],Setup)
    universe = Generator.generate_simplified_models(10)

    meaning = Generator.MeaningCalculator(universe)(expression)

    measurer = MonotonicityMeasurer(universe, 10, 'A')

    monotonicity = measurer(meaning)

    assert not math.isclose(monotonicity, 1)

def test_not_entirely_upward_monotone_a_equals():
    expression = Parser.parse_expression(['or',['=',['card',['intersection','A','B']],3],['=',9,['card',['intersection','A','B']]]],Setup)
    universe = Generator.generate_simplified_models(10)

    meaning = Generator.MeaningCalculator(universe)(expression)

    measurer = MonotonicityMeasurer(universe, 10, 'A')

    monotonicity = measurer(meaning)
    print(monotonicity)
    assert not math.isclose(monotonicity, 1)

