def measure_complexity(expression):
    return expression.length()/10


def measure_communicative_cost(expression, universe):
    true_count = 0
    for model in universe:
        if expression.evaluate(model):
            true_count += 1
    return true_count / len(universe) if true_count > 0 else 1
