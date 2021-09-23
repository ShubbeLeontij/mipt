#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import matplotlib.pyplot as plt

def func(x):
    numer = 1 / (np.exp(np.sin(x + 1)))
    denom = 5 / 4 + np.power(x, 15)
    return (np.log(numer / denom) / (np.log(1 + np.power(x, 2)))

x_arr = np.array([1, 10, 1000])
print(*func(x_arr))


# In[14]:


x = np.arange(1, 10.01, 0.1)
plt.plot(x, func(x))
plt.show()


# In[ ]:




