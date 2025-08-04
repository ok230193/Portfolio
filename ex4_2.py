from matplotlib import pyplot as plt
import numpy as np


def plot_numerical_solution():
    y = 0
    x = 0
    h = 0.1
    x_list = []
    y_list = []
    while x < 4 * np.pi:
        x_list.append(x)
        y_list.append(y)
        y = y + h * np.cos(x)
        x += h
    plt.plot(x_list, y_list)


def plot_analytical_solution():
    x = 0
    h = 0.1
    x_list = []
    y_list = []
    while x < 4 * np.pi:
        x_list.append(x)
        y_list.append(np.sin(x))
        x += h
    plt.plot(x_list, y_list)


def main():
    plot_analytical_solution()
    plot_numerical_solution()
    plt.show()


if __name__ == '__main__':
    main()