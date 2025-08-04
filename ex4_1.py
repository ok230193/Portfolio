from matplotlib import pyplot as plt


def plot_numerical_solution():
    y = 1
    x = 0
    h = 0.05
    x_list = []
    y_list = []
    while x <= 0.5:
        x_list.append(x)
        y_list.append(y)
        x += h
        y = y + h * y ** 2
    plt.plot(x_list, y_list)


def plot_analytical_solution():
    y = 1
    x = 0
    h = 0.05
    x_list = []
    y_list = []
    while x <= 0.5:
        x_list.append(x)
        y_list.append(y)
        x += h
        y = 1 / (1 - x)
    plt.plot(x_list, y_list)


def main():
    plot_analytical_solution()
    plot_numerical_solution()
    plt.show()


if __name__ == '__main__':
    main()
