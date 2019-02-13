class Expression:

    def __init__(self, name, func, *arg_expressions):
        self.name = name
        self.func = func
        self.arg_expressions = arg_expressions

    def length(self):
        total_length = 1
        for arg_expression in self.arg_expressions:
            total_length += arg_expression.length()
        return total_length

    def evaluate(self, model):
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
            return "{0}({1},{2})".format(self.name, self.arg_expressions[0], self.arg_expressions[1])

    def to_name_structure(self):
        if len(self.arg_expressions) is 0:
            return self.name

        return [self.name, *[expression.to_name_structure() for expression in self.arg_expressions]]


class Primitives:

    @staticmethod
    def create_set_func(set_name):
        return lambda model: model.get_set(set_name)

    @staticmethod
    def create_value_func(number):
        return lambda model: number