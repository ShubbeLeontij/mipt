#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import matplotlib.pyplot as plt

def func(function, x):
    return eval(function)

#with plt.xkcd():
function = input()
x_min = -10
x_max = 10
step = 0.001
x_arr = np.arange(x_min, x_max, step)
plt.plot(x_arr, func(function, x_arr))
plt.show()


# In[ ]:




