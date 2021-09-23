#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import matplotlib.pyplot as plt

def func(x):
    return (x * x - x - 6)

x_min = -3
x_max = 3.5
step = 0.001
x_arr = np.arange(x_min, x_max, step)
plt.plot(x_arr, func(x_arr))
plt.plot([x_min, x_max], [0, 0])
plt.show()


# In[ ]:




