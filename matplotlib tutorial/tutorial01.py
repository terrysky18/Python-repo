"""
Tutorial for beginners in Matplotlib
Pyplot function tutorial
"""

import matplotlib.pyplot as plt

# set line width
plt.plot([1, 2, 3, 4], linewidth=2.0)

# third argument of plot is the format string
# letter and symbols of format string are from MATLAB
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'r*')
plt.ylabel('some numbers')
plt.show()

