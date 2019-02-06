from enum import Enum


class Primitive(Enum):
    M = 1
    A = 2
    B = 3


class GeneralizedQuantifierModel:

    def __init__(self, M, A, B):
        self.M = M
        self.A = A
        self.B = B

    def get_primitive_value(self, primitive):
        if primitive == Primitive.A:
            return self.A
        if primitive == Primitive.B:
            return self.B
        if primitive == Primitive.M:
            return self.M
        raise ValueError('Invalid primitive value: {0}'.format(primitive))
