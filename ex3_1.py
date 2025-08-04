import matplotlib.pyplot as plt


def f(x):
    return x ** 2 - 3


def main():
    x1 = 10
    x2 = 0
    e = 0.0001
    x3_list = []

    while True:
        x3 = x1 + x2
        x3 /= 2
        x3_list.append(x3)

        if f(x2) * f(x3) < 0:
            x1 = x3
        else:
            x2 = x3

        if abs(x2 - x1) < e:
            break

    plt.plot(x3_list)
    plt.show()


if __name__ == '__main__':
    main()
