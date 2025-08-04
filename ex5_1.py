import matplotlib.pylab as plt
import numpy as np


def plot_numerical_solution():
    h = 0.05
    x = 0
    x_max = 3
    y = 1
    y_list = []
    x_list = []

    while x <= x_max:
        y_list.append(y)
        x_list.append(x)
        k1 = h * (-2 * x * y)
        k2 = h * (-2 * (x + h/2) * (y + k1/2))
        k3 = h * (-2 * (x + h/2) * (y + k2/2))
        k4 = h * (-2 * (x + h) * (y + k3))
        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x += h
    plt.plot(x_list, y_list, '.')


def plot_analytical_solution():
    y = 1
    h = 0.05
    y_list = []
    x_list = []
    x = 0
    x_max = 3
    while x <= x_max:
        x_list.append(x)
        x += h
        y_list.append(y)
        y = np.exp(-x**2)
    plt.plot(x_list, y_list)


def main():
    plot_numerical_solution()
    plot_analytical_solution()
    plt.show()


if __name__ == '__main__':
    main()
