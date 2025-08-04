import matplotlib.pylab as plt


def main():
    h = 0.1
    t_max = 30
    g = 9.80665
    k = 0.01
    v = 30
    t = 0
    v_list = []
    t_list = []

    while t < t_max:
        t_list.append(t)
        v_list.append(v)
        k1 = h * (-g + k * v ** 2)
        k2 = h * (-g + k * ((v + k1 / 2) ** 2))
        k3 = h * (-g + k * ((v + k2 / 2) ** 2))
        k4 = h * (-g + k * ((v + k3) ** 2))
        v = v + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += h
    t_list.append(t)
    v_list.append(v)
    plt.plot(t_list, v_list)
    plt.show()


if __name__ == "__main__":
    main()
