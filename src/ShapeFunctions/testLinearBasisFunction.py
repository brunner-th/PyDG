import numpy as np
import matplotlib.pyplot as plt
from ShapeFunctions.LinearBasisFunction import LinearBasisFunction


x_node = np.array([1, 1, 2])
y_node = np.array([1, 2, 1])

plt.plot(x_node, y_node)


value, gradx, grady = LinearBasisFunction().evaluateLinearBasisFunction(x_node, y_node, 0.5, 0.5)

plt.plot(1.2, 1.2, 'ro')


area, gradx2, grady2 = LinearBasisFunction().evalulateGradientsLinearBasisFunction(x_node, y_node)


plt.show()