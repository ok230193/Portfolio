import matplotlib.pyplot as plt


def f(x):
    return 3 * x ** 4 - 2 * x ** 3 + x ** 2 - 4 * x - 50


def main():
    x1 = 4
    x2 = 0
    e = 0.00001
    x3_list = []

    while True:
        x3 = ((x1 + x2) / 2)
        x3_list.append(x3)

        if f(x2) * f(x3) < 0:
            x1 = x3
        else:
            x2 = x3

        if abs(x2 - x1) < e:
            break

    plt.plot(x3_list)
    plt.show()
    print(x3_list)
    print(f(x3_list[-1]))


if __name__ == '__main__':
    main()
