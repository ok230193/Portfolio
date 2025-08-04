import numpy as np


def jacobi_method():
    a = np.array([[4, 1, -2], [1, 6, 3], [2, 1, 9]])
    b = np.array([[6], [-2], [-7]])
    x = np.zeros((3, 1))
    epsilon = 0.0001
    d = np.diag(np.diag(a))

    sum = 0
    while np.linalg.norm(b - a @ x) / np.linalg.norm(b) > epsilon:
        sum += 1
        x = np.linalg.inv(d) @ (b - (a - d) @ x)

    return x, sum


def main():
    x, sum = jacobi_method()
    print(f"解：{x}")
    print(f"更新回数：{sum}")


if __name__ == '__main__':
    main()
