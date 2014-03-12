import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

h = [186, 176, 158, 180, 186, 168, 168, 164, 178, 170, 189, 195, 172,
     187, 180, 186, 185, 168, 179, 178, 183, 179, 170, 175, 186, 159,
     161, 178, 175, 185, 175, 162, 173, 172, 177, 175, 172, 177, 180]

std = np.std(h) 
mean = np.mean(h)    
plt.plot(norm.pdf(h,mean,std))
plt.show()