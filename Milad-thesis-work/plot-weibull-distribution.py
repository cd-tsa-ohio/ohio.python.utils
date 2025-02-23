import matplotlib as plt
import numpy as np

x=np.seq(1,15,0.1)
plt.plot(dweibull(x, shape= 3.2, scale=5.6), type="l", col= "red")
