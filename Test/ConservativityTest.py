import math

import Generator
import Parser
from Conservativity import ConservativityMeasurer


class Setup:
    parse_primitive = Parser.parse_simple_primitive_with_sets


def test_completely_A_conservative():
    spec = [">",["card",["diff","B","A"]],["card",["intersection","A","B"]]]
    expression = Parser.parse_expression(spec,Setup)

    universe = Generator.generate_simplified_models(10)
    meaning = Generator.MeaningCalculator(universe)(expression)

    measurer = ConservativityMeasurer(universe,10,'A')

    conservativity = measurer(meaning)

    assert math.isclose(conservativity, 1)

def test_semi_A_conservative():
    spec = ["and",[">",["card","A"],2],[">",["card",["diff","B","A"]],["card",["intersection","A","B"]]]]
    expression = Parser.parse_expression(spec,Setup)

    universe = Generator.generate_simplified_models(10)
    meaning = Generator.MeaningCalculator(universe)(expression)

    measurer = ConservativityMeasurer(universe,10,'A')

    conservativity = measurer(meaning)

    assert not math.isclose(conservativity, 1) and not math.isclose(conservativity, 0)

def test_completely_not_B_conservative():
    spec = [">",["card",["diff","B","A"]],["card",["intersection","A","B"]]]
    expression = Parser.parse_expression(spec,Setup)

    universe = Generator.generate_simplified_models(10)
    meaning = Generator.MeaningCalculator(universe)(expression)

    measurer = ConservativityMeasurer(universe,10,'B')

    conservativity = measurer(meaning)

    assert math.isclose(conservativity, 0)

def test_completely_B_conservative():
    spec = [">",["card",["diff","A","B"]],["card",["intersection","A","B"]]]
    expression = Parser.parse_expression(spec,Setup)

    universe = Generator.generate_simplified_models(10)
    meaning = Generator.MeaningCalculator(universe)(expression)

    measurer = ConservativityMeasurer(universe,10,'B')

    conservativity = measurer(meaning)

    assert math.isclose(conservativity, 1)
