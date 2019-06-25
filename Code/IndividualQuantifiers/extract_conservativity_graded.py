import analysisutil

analysisutil.add_argument('threshold', type=float)

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

threshold = round(args.threshold, 2)

conservativities = file_util.load_dill('conservativities_b.dill')
indices = set(i for (i, conservativity) in enumerate(conservativities) if conservativity > threshold)

file_util.dump_dill(indices, 'conservative_{0}_expression_indices.dill'.format(threshold))
