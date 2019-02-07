from collections import namedtuple

Operator = namedtuple("Operator", "func inputTypes outputType")

operators = {
    "subset": Operator(
        lambda model, x, y: x <= y,
        [set,set],
        bool
    ),
    ">": Operator(
        lambda model, x, y: x > y,
        [float,float],
        bool
    ),
    ">i": Operator(
        lambda model, x, y: x > y,
        [int,int],
        bool
    ),
    "/": Operator(
        lambda model, x, y: x / y if y > 0 else 0,
        [int,int],
        float
    ),
    "diff": Operator(
        lambda model, x, y: x - y,
        [set,set],
        set
    ),
    "card": Operator(
        lambda model, x: len(x),
        [set],
        int
    ),
    "intersection": Operator(
        lambda model, x, y: x & y,
        [set, set],
        set
    ),
    "union": Operator(
        lambda model, x, y: x | y,
        [set, set],
        set
    ),
    "and": Operator(
        lambda model, x, y: x and y,
        [bool, bool],
        bool
    ),
    "or": Operator(
        lambda model, x, y: x or y,
        [bool, bool],
        bool
    )
}

operatorsByReturnType = {
    set: [],
    bool: [],
    float: [],
    int: []
}
for (name, operator) in operators.items():
    operatorsByReturnType[operator.outputType].append((name,operator))
