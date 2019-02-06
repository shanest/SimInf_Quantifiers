from abc import ABC, abstractmethod
from GeneralizedQuantifierModel import Primitive

class Expression(ABC):

    @abstractmethod
    def evaluate(self, model):
        pass

    @abstractmethod
    def length(self):
        pass


class PrimitiveExpression(Expression):

    def __init__(self, primitive_string):
        self.primitive = Primitive[primitive_string]

    def evaluate(self, model):
        return model.get_primitive_value(self.primitive)

    def length(self):
        return 1


class SubsetExpression(Expression):

    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression

    def evaluate(self, model):
        left_set = self.left_expression.evaluate(model)
        right_set = self.right_expression.evaluate(model)

        return left_set <= right_set

    def length(self):
        return 1 + self.left_expression.length() + self.right_expression.length()


class NumberExpression(Expression):

    def __init__(self, number):
        self.number = number

    def evaluate(self, model):
        return self.number

    def length(self):
        return 1


class GreaterThanExpression(Expression):

    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression

    def evaluate(self, model):
        left_num = self.left_expression.evaluate(model)
        right_num = self.right_expression.evaluate(model)

        return left_num > right_num

    def length(self):
        return 1 + self.left_expression.length() + self.right_expression.length()


class MinusExpression(Expression):

    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression

    def evaluate(self, model):
        left_value = self.left_expression.evaluate(model)
        right_value = self.right_expression.evaluate(model)

        return left_value - right_value

    def length(self):
        return 1 + self.left_expression.length() + self.right_expression.length()


class CardinalityExpression(Expression):

    def __init__(self, set_expression):
        self.set_expression = set_expression

    def evaluate(self, model):
        set_value = self.set_expression.evaluate(model)

        return len(set_value)

    def length(self):
        return 1 + self.set_expression.length()
