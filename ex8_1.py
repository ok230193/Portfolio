def main():
    A = 13
    B = 5
    M = 24
    x0 = 1
    n = 30
    x_list = lcg(A, B, M, x0, n)
    print(x_list)


def lcg(a, b, m, x0, n):
    x_list = [x0]
    x = x0
    for i in range(1, n):
        x = (a * x + b) % m
        x_list.append(x)
    return x_list


if __name__ == "__main__":
    main()
