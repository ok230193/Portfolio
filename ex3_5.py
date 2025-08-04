import matplotlib.pyplot as plt
import math

import numpy as np


def main():
    xd = np.linspace(np.pi * -2, np.pi * 2, 400)
    h = 0.001

    fd = (np.sin(xd + h) - np.sin(xd - h)) / (2 * h)

    plt.plot(xd, fd)
    plt.show()


if __name__ == '__main__':
    main()
