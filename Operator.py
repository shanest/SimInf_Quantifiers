from collections import namedtuple

Operator = namedtuple("Operator", "func inputTypes outputType")

operators = {
    # "subset": Operator(
    #     lambda model, x, y: x <= y,
    #     [set,set],
    #     bool
    # ),
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
    # "diff": Operator(
    #     lambda model, x, y: x - y,
    #     [set,set],
    #     set
    # ),
    # "card": Operator(
    #     lambda model, x: len(x),
    #     [set],
    #     int
    # ),
    # "intersection": Operator(
    #     lambda model, x, y: x & y,
    #     [set, set],
    #     set
    # ),
    # "union": Operator(
    #     lambda model, x, y: x | y,
    #     [set, set],
    #     set
    # ),
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
    # "empty": Operator(
    #     lambda model, x: len(x) is 0,
    #     [set],
    #     bool
    # )
    # "A": Operator(
    #     lambda model: model.A,
    #     [],
    #     int
    # ),
    # "B": Operator(
    #     lambda model: model.B,
    #     [],
    #     int
    # ),
    # "A-B": Operator(
    #     lambda model: model.AminusB,
    #     [],
    #     int
    # ),
    # "A&B": Operator(
    #     lambda model: model.AandB,
    #     [],
    #     int
    # ),
}

operatorsByReturnType = {
    set: [],
    bool: [],
    float: [],
    int: []
}

possibleInputTypes = []

for (name, operator) in operators.items():
    operatorsByReturnType[operator.outputType].append((name,operator))
    possibleInputTypes.append(operator.inputTypes)
