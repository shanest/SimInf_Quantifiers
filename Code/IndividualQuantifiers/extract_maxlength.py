import analysisutil

analysisutil.add_argument('length', type=int)
(args, setup, file_util) = analysisutil.init(use_base_dir=True)

expressions = file_util.load_dill('expressions.dill')

indices = [i for (i, expr) in enumerate(expressions) if expr.length() <= args.length]

file_util.dump_dill(indices, 'upto{0}_expression_indices.dill'.format(args.length))