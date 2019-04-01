from analysisutil import file_util, args
import matplotlib.pyplot as plt

informativeness = file_util.load_dill('informativeness_{0}.dill'.format(args.informativeness_strategy))
complexity = file_util.load_dill('complexity_{0}.dill'.format(args.complexity_strategy))


plt.plot(informativeness,complexity,'o')
#plt.axis([0,1,0,1])

plt.show()
