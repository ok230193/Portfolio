import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def jacobi_method():
    a = np.array([
        [4, -1, 0, -1, 0, 0, 0, 0, 0],
        [-1, 4, -1, 0, -1, 0, 0, 0, 0],
        [0, -1, 4, 0, 0, -1, 0, 0, 0],
        [-1, 0, 0, 4, -1, 0, -1, 0, 0],
        [0, -1, 0, -1, 4, -1, 0, -1, 0],
        [0, 0, -1, 0, -1, 4, 0, 0, -1],
        [0, 0, 0, -1, 0, 0, 4, -1, 0],
        [0, 0, 0, 0, -1, 0, -1, 4, -1],
        [0, 0, 0, 0, 0, -1, 0, -1, 4]])
    b = np.array([[0], [0], [0.25], [0], [0], [0.5], [0.25], [0.5], [1.5]])
    d = np.diag(np.diag(a))
    x = np.zeros((9, 1))
    epsilon = 0.000000001

    while np.linalg.norm(b - a @ x) / np.linalg.norm(b) > epsilon:
        x = np.linalg.inv(d) @ (b - (a - d) @ x)

    u = np.array([[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0.25],
                  [0, 0, 0, 0, 0.5],
                  [0, 0, 0, 0, 0.75],
                  [0, 0.25, 0.5, 0.75, 1]])
    u[1:4, 1:4] = x.reshape((3, 3))
    return u


def plot_laplace(u):
    h = 0.25
    x = np.linspace(0.0, 1.0, int(1.0 / h + 1))
    y = np.linspace(0.0, 1.0, int(1.0 / h + 1))
    xv, yv = np.meshgrid(x, y)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(xv, yv, u, cmap=mpl.colormaps["coolwarm"])
    plt.show()


def main():
    u = jacobi_method()
    print(u)
    plot_laplace(u)


if __name__ == '__main__':
    main()
