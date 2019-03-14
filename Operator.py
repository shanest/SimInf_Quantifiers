from collections import namedtuple
from functools import lru_cache

from SetPlaceholders import SetPlaceholder
import SetPlaceholders
from GeneralizedQuantifierModel import get_cardinality, subset

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
    "diff": Operator(
        lambda model, x, y: SetPlaceholders.minus(x,y),
        (SetPlaceholder,SetPlaceholder),
        SetPlaceholder
    ),
    "card": Operator(
        lambda model, x: get_cardinality(model, x),
        SetPlaceholder,
        int
    ),
    "intersection": Operator(
        lambda model, x, y: SetPlaceholders.intersection(x,y),
        (SetPlaceholder, SetPlaceholder),
        SetPlaceholder
    ),
    "union": Operator(
        lambda model, x, y: SetPlaceholders.union(x,y),
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
        (SetPlaceholder),
        bool
    )
}
