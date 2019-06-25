import argparse
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import Generator

parser = argparse.ArgumentParser(description="Vizualize Random Meaning")
parser.add_argument('model_size', type=int)
args = parser.parse_args()

universe = Generator.generate_simplified_models(args.model_size)
A = []
B = []
AandB = []

A_false = []
B_false = []
AandB_false = []

for model in universe:
    if random.choice([True, False]):
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
ax.set_title('Random')

plt.show()