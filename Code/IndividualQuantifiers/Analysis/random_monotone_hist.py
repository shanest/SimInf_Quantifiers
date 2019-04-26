import random

from pathos.multiprocessing import ProcessPool

import Generator
from Monotonicity import MonotonicityMeasurer
import matplotlib.pyplot as plt

universe = Generator.generate_simplified_models(10)

meanings = [tuple(random.choice([True, False]) for i in range(len(universe))) for j in range(5000)]

measurer_up = MonotonicityMeasurer(universe, 10, 'B')
measurer_down = MonotonicityMeasurer(universe, 10, 'B', down=True)

with ProcessPool(4) as process_pool:
    monotonicities_up = process_pool.map(measurer_up, meanings)
    monotonicities_down = process_pool.map(measurer_down, meanings)
    monotonicities = process_pool.map(max, monotonicities_up, monotonicities_down)


plt.hist(monotonicities,bins=30,range=[0,1])

plt.show()
