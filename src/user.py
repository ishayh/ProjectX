from src.location import Location

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits.axisartist import Axes


class User:
    def __init__(self, config):
        # self.start_loc = [40.7829, -73.9654]
        # self.end_loc = self.start_loc
        # self.distance = 10
        self.start_loc = config['startLocation']
        self.end_loc = self.start_loc
        self.distance = config['distance']

    def process_user_setting(self):
        print ("in process_user_setting: start loc is " + str(self.start_loc[0]) + str(self.start_loc[1]))
        location = Location(self.start_loc[0], self.start_loc[1])
        ax = host_subplot(111, axes_class=Axes)

        ax.set_autoscale_on(True)

        latitude1, longitude1 = location.x0, location.y0  # type: (float, float)
        ax.plot(latitude1, longitude1, 'ro')

        location = Location(latitude1, longitude1)

        x, y = location.find_hottest_route()
        print("after find_hottest_route= " + str(x), str(y))
        ax.plot(x, y, 'bo')
        plt.show()
        return x, y


# config = 0
# user = User(config)
# user.process_user_setting()
