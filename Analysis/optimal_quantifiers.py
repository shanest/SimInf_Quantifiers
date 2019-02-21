import pickle

import Parser

quantifiers = list(Parser.load_from_file('../results/GeneratedQuantifiers.json').values())
with open('../results/generated_meanings.pickle', 'rb') as file:
    raw_meanings = pickle.load(file)

universe_size = 20