#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
import matplotlib.pyplot as plt

def func(x):
    numer = np.log((np.power(x, 2) + 1) * (np.exp(-(np.absolute(x)) / 10)))
    denom = 1 + np.tan(1 / (1 + np.power(np.sin(x), 2)))
    return (numer / denom)

x_min = -10
x_max = 10
step = 0.001
x_arr = np.arange(x_min, x_max, step)
plt.plot(x_arr, func(x_arr))
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




