from collections import namedtuple
from functools import lru_cache

SetPlaceholder = namedtuple("SetPlaceholder","name")

A = SetPlaceholder("A")
B = SetPlaceholder("B")
AminusB = SetPlaceholder("A-B")
BminusA = SetPlaceholder("B-A")
AandB = SetPlaceholder("A&B")
AunionB = SetPlaceholder("A|B")
AunionBminusAandB = SetPlaceholder("A|B-A&B")
empty = SetPlaceholder("0")

representation = {
    A: frozenset({AminusB,AandB}),
    B: frozenset({AandB,BminusA}),
    AminusB: frozenset({AminusB}),
    BminusA: frozenset({BminusA}),
    AandB: frozenset({AandB}),
    AunionB: frozenset({AminusB, AandB, BminusA}),
    AunionBminusAandB: frozenset({AminusB,BminusA}),
    empty: frozenset({})
}

placeholder_by_representation = {v: k for k,v in representation.items()}


def apply(func, X, Y):
    return placeholder_by_representation[frozenset(func(representation[X],representation[Y]))]


def minus(X, Y):
    return apply(lambda x, y: x - y, X, Y)


def intersection(X, Y):
    return apply(lambda x, y: x & y, X, Y)


def union(X, Y):
    return apply(lambda x, y: x | y, X, Y)