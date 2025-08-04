import matplotlib.pyplot as plt


def main():
    h = 0.01
    g = 9.80665
    x = 35
    v = 30
    t = 0
    t_list = []
    x_list = []
    while x >= 0:
        t_list.append(t)
        x_list.append(x)
        t += h
        x = x + h * v
        v = v - h * g
    plt.plot(t_list, x_list)
    plt.show()


if __name__ == '__main__':
    main()
