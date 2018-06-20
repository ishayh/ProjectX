import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits.axisartist import Axes


class Location:
    def __init__(self, x0, y0):
        self.x0 = x0
        self.y0 = y0

    def get_random_point(self, radius):
        a = self.x0
        b = self.y0
        r = radius

        x_min = a - r
        x_max = a + r
        x_range = x_max - x_min

        x1 = x_min + np.random.uniform(0, 1) * x_range

        y_delta = np.sqrt(np.power(r, 2) - np.power((x1 - a), 2))
        y_max = b + y_delta
        y_min = b - y_delta
        y_range = y_max - y_min

        y1 = y_min + np.random.uniform(0, 1)*y_range

        return x1, y1


# fig = plt.figure()
# ax = host_subplot(111, axes_class=Axes)
#
# ax.set_autoscale_on(True)
#
# latitude1, longitude1 = 20, 10 # type: (float, float)
# ax.plot(latitude1, longitude1, 'ro')
#
# location = Location(latitude1, longitude1)
#
# for i in range(1, 1000):
#     x, y = location.get_random_point(500)
#     ax.plot(x, y, 'bo')
# plt.show()