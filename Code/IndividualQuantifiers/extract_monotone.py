from pathos.multiprocessing import ProcessPool

import Generator
import analysisutil

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

expressions = file_util.load_dill('expressions.dill')
raw_meanings = file_util.load_dill('meanings.dill')

universe = Generator.generate_simplified_models(args.model_size)


def flip_model(model):
    return Generator.SimplifiedQuantifierModel(model.B, model.A, model.B - model.AandB, model.AandB)


def get_monotone_quantifiers(monotone_set, direction, process_pool):

    flip_model_if_needed = flip_model if monotone_set is 'B' else lambda model: model

    meanings = [[[[None]*(args.model_size-B+1) for AandB in range(B+1)] for B in range(args.model_size+1)]
                for i in range(len(raw_meanings))]

    for (i,raw_meaning) in enumerate(raw_meanings):
        for (j, model) in enumerate(universe):
            model = flip_model_if_needed(model)
            meanings[i][model.B][model.AandB][model.AminusB] \
            = raw_meaning[j] if direction is 'up' else not raw_meaning[j]

    def check_monotone(meaning):
        is_monotone = [[[None]*(args.model_size-B+1) for AandB in range(B+1)] for B in range(args.model_size+1)]

        def check_monotone_inner(meaning, B, AandB, AminusB, truth_found):
            if truth_found:
                if not meaning[B][AandB][AminusB]:
                    return False
                if AandB + AminusB is args.model_size:
                    return True
                if AminusB is args.model_size-B:
                    return check_monotone(meaning, B, AandB + 1, AminusB, True)
                if AandB is B:
                    return check_monotone(meaning, B, AandB, AminusB + 1, True)
                return check_monotone(meaning, B, AandB+1, AminusB, True) and check_monotone(meaning, B, AandB, AminusB+1, True)

            else:
                if AandB + AminusB is args.model_size:
                    return True

                if meaning[B][AandB][AminusB]:
                    return check_monotone(meaning, B, AandB, AminusB, True)

                if AminusB is args.model_size-B:
                    return check_monotone(meaning, B, AandB + 1, AminusB)

                if AandB is B:
                    return check_monotone(meaning, B, AandB, AminusB + 1)

                return check_monotone(meaning, B, AandB + 1, AminusB) and check_monotone(meaning, B, AandB, AminusB + 1)

        def check_monotone(meaning, B, AandB=0, AminusB=0, truth_found=False):
            if is_monotone[B][AandB][AminusB] is None:
                is_monotone[B][AandB][AminusB] = check_monotone_inner(meaning,B,AandB,AminusB,truth_found)

            return is_monotone[B][AandB][AminusB]

        monotone = True
        for B in range(args.model_size+1):
            if not check_monotone(meaning, B):
                monotone = False
                break

    is_monotone = process_pool.map(check_monotone, meanings)
    return set(i for (i, val) in enumerate(is_monotone) if val)


with ProcessPool(nodes=args.processes) as process_pool:
    a_up = get_monotone_quantifiers('A','up', process_pool)
    b_up = get_monotone_quantifiers('B','up', process_pool)
    a_down = get_monotone_quantifiers('A','down', process_pool)
    b_down = get_monotone_quantifiers('B','down', process_pool)

indices = a_up.union(b_up).union(a_down).union(b_down)

file_util.dump_dill(indices,'monotone_expression_indices.dill')
