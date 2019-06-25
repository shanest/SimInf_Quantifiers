import math

import Operator
import Parser
from Measurer import SpecialComplexityMeasurer

class Setup:
    parse_primitive = Parser.parse_simple_primitive_with_sets


def test_not_entirely_upward_monotone_a():
    expression = Parser.parse_expression(['>',['card',['intersection','A','B']],2],Setup)
    operators = ['>','/','card','intersection']

    measurer = SpecialComplexityMeasurer({op: Operator.operators[op] for op in operators}, 4)

    complexity = measurer(expression)

    print(complexity)
    assert not math.isclose(complexity, 1 - 1/(1 + math.exp(2*1/1/2/3/3/3/3)))