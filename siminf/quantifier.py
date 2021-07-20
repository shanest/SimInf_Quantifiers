from siminf.expression import Expression
from siminf.generalized_quantifier_model import GeneralizedQuantifierModel


class Quantifier:

    def __init__(self, expression: Expression, presupposition: Expression =None):
        self.expression = expression
        self.presupposition = presupposition
        self.has_presupposition = presupposition is not None

    def evaluate(self, model: GeneralizedQuantifierModel):
        if self.has_presupposition and not self.presupposition.evaluate(model):
            return None

        return self.expression.evaluate(model)

    def __str__(self):
        return "P:{0} E:{1}".format(self.presupposition, self.expression)

    def to_name_structure(self):
        presupposition_structure = self.presupposition.to_name_structure() if self.has_presupposition else None

        return {
            "presupposition": presupposition_structure,
            "expression": self.expression.to_name_structure()
        }
