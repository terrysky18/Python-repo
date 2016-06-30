"""
Second tutorial for MatPlotLib beginner

The example demonstrates plotting several lines with different format
styles in one command using arrays
"""

import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 200ms intervals
# from 0 to 5 at step of 0.2
t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
plt.show()

