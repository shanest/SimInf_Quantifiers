import argparse
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import Generator
import analysisutil

(args, setup, file_util) = analysisutil.init(use_base_dir=True)

meanings = file_util.load_dill('meanings.dill')
expressions = file_util.load_dill('expressions.dill')
(meaning, expression) = random.choice(list(zip(meanings, expressions)))

universe = Generator.generate_simplified_models(args.model_size)


A = []
B = []
AandB = []

A_false = []
B_false = []
AandB_false = []

for (i, model) in enumerate(universe):
    if meaning[i]:
        A.append(model.A)
        B.append(model.B)
        AandB.append(model.AandB)
    else:
        A_false.append(model.A)
        B_false.append(model.B)
        AandB_false.append(model.AandB)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(A,B,AandB)
ax.scatter(A_false,B_false,AandB_false, c='red')

ax.set_xlabel('A')
ax.set_ylabel('B')
ax.set_zlabel('A & B')
ax.set_title(str(expression))

plt.show()