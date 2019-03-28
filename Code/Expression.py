from functools import lru_cache


class Expression:

    def __init__(self, name, func, *arg_expressions, is_constant=None):
        self.name = name
        self.func = func
        self.arg_expressions = arg_expressions
        self.internal_length = None

        if is_constant is None:
            args_constant = [arg.is_constant for arg in arg_expressions]
            self.is_constant = len(args_constant) is not 0 and False not in args_constant
        else:
            self.is_constant = is_constant

        if self.is_constant:
            self.constant_value = func(None,*[arg_expression.evaluate(None) for arg_expression in arg_expressions])

    def length(self):
        if self.internal_length is not None:
            return self.internal_length
        total_length = 1
        for arg_expression in self.arg_expressions:
            total_length += arg_expression.length()
        self.internal_length = total_length
        return total_length

    def evaluate(self, model):
        if self.is_constant:
            return self.constant_value

        arg_values = []
        for arg_expression in self.arg_expressions:
            arg_values.append(arg_expression.evaluate(model))
        return self.func(model, *arg_values)

    def __str__(self):
        if len(self.arg_expressions) is 0:
            return str(self.name)
        if len(self.arg_expressions) is 1:
            return "{0}({1})".format(self.name, self.arg_expressions[0])
        if len(self.arg_expressions) is 2:
            return "{0}({1},{2})".format(self.name, *self.arg_expressions)
        if len(self.arg_expressions) is 3:
            return "{0}({1},{2},{3})".format(self.name, *self.arg_expressions)
        if len(self.arg_expressions) is 4:
            return "{0}({1},{2},{3},{4})".format(self.name, *self.arg_expressions)

    def to_name_structure(self):
        if len(self.arg_expressions) is 0:
            return self.name

        return [self.name, *[expression.to_name_structure() for expression in self.arg_expressions]]


class Primitives:

    cardinality_functions = {
        'A': lambda model: model.A,
        'B': lambda model: model.B,
        'A-B': lambda model: model.AminusB,
        'A&B': lambda model: model.AandB
    }

    @staticmethod
    def create_set_func(set_name):
        return lambda model: model.get_set(set_name)

    @staticmethod
    def create_value_func(number):
        return lambda model: number
