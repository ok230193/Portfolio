import matplotlib.pyplot as plt


def main():
    h = 0.01
    g = 9.80665
    x = 55
    v = 19.6
    t = 0
    p = 0
    t_list = []
    x_list = []
    while x >= 0:
        t_list.append(t)
        x_list.append(x)
        t += h
        x = x + h * v
        v = v - h * g
        if x == 74.6847664999999 and p != -1:
            print(t)
            p = -1

    plt.plot(t_list, x_list)
    plt.show()


if __name__ == '__main__':
    main()
