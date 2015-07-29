#!/usr/bin/env python
"""Short Description"""

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

import numpy as np


y = np.array([[1, 0, 0, 0, 0, 4], [2, 0, 0, 0, 0, 9]])
x = np.array([1, 2])

print y

n = np.max(x.shape)    
print n

A = np.vstack([x, np.ones(len(x))]).T
print A

m, c = np.linalg.lstsq(A, y)[0]

print m



