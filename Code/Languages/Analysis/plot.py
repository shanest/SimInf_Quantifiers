from analysisutil import file_util
import matplotlib.pyplot as plt

informativeness = file_util.load_dill('informativeness.dill')
complexity = file_util.load_dill('complexity.dill')


plt.plot(informativeness,complexity,'o')
#plt.axis([0,1,0,1])

plt.show()
