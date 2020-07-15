import math
from collections import namedtuple

#from SetPlaceholders import SetPlaceholder
from siminf.set_place_holders import SetPlaceholder # to replace from SetPlaceholders import SetPlaceholder

#import SetPlaceholders
from siminf import set_place_holders as sph #to replace import SetPlaceholders

#from GeneralizedQuantifierModel import get_cardinality, subset
from siminf.generalized_quantifier_model import get_cardinality, subset # to replace from GeneralizedQuantifierModel import get_cardinality, subset

Operator = namedtuple("Operator", "func inputTypes outputType")

operators = {
    "subset": Operator(
        lambda model, x, y: subset(model,x,y),
        (SetPlaceholder,SetPlaceholder),
        bool
    ),
    ">f": Operator(
        lambda model, x, y: x > y,
        (float,float),
        bool
    ),
    "=f": Operator(
        lambda model, x, y: math.isclose(x,y),
        (float,float),
        bool
    ),
    ">": Operator(
        lambda model, x, y: x > y,
        (int,int),
        bool
    ),
    ">=": Operator(
        lambda model, x, y: x >= y,
        (int,int),
        bool
    ),
    "=": Operator(
        lambda model, x, y: x is y,
        (int,int),
        bool
    ),
    "/": Operator(
        lambda model, x, y: x / y if y > 0 else 0,
        (int,int),
        float
    ),
    "-": Operator(
        lambda model, x, y: x - y,
        (int,int),
        int
    ),
    "+": Operator(
        lambda model, x, y: x + y,
        (int, int),
        int
    ),
    "diff": Operator(
        lambda model, x, y: sph.minus(x, y),
        (SetPlaceholder,SetPlaceholder),
        SetPlaceholder
    ),
    "card": Operator(
        lambda model, x: get_cardinality(model, x),
        SetPlaceholder,
        int
    ),
    "intersection": Operator(
        lambda model, x, y: sph.intersection(x, y),
        (SetPlaceholder, SetPlaceholder),
        SetPlaceholder
    ),
    "union": Operator(
        lambda model, x, y: sph.union(x, y),
        (SetPlaceholder, SetPlaceholder),
        SetPlaceholder
    ),
    "and": Operator(
        lambda model, x, y: x and y,
        (bool, bool),
        bool
    ),
    "or": Operator(
        lambda model, x, y: x or y,
        (bool, bool),
        bool
    ),
    "not": Operator(
        lambda model, x: not x,
        (bool),
        bool
    ),
    "empty": Operator(
        lambda model, x: get_cardinality(model, x) is 0,
        SetPlaceholder,
        bool
    ),
    "nonempty": Operator(
        lambda model, x: get_cardinality(model, x) > 0,
        SetPlaceholder,
        bool
    ),
    "proportion": Operator(
        lambda model, X, Y, q: get_cardinality(model, X) / get_cardinality(model, Y) > q if get_cardinality(model, Y) > 0 else 0,
        (SetPlaceholder,SetPlaceholder,float),
        bool
    ),
    "%": Operator(
        lambda model, x, y: x % y if y > 0 else 0,
        (int, int),
        int
    )
}
