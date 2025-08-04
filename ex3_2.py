import matplotlib.pyplot as plt


def f(x):
    return x ** 2 - 3


def df(x):
    return 2 * x


def main():
    x0 = 10
    e = 0.0001
    x_list = [x0]

    while True:
        x1 = x0 - (f(x0) / df(x0))
        x_list.append(x1)

        if abs(x1 - x0) < e:
            break
        x0 = x1

    plt.plot(x_list)
    plt.show()


if __name__ == '__main__':
    main()
