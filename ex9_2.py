import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.animation as animation


def random_walk():
    trials = 200
    steps = 100
    trajectories = np.zeros((trials, steps))
    choices = [1, -1]
    np.random.seed(0)


    for trial in range(trials):
        for step in range(1, steps):
            trajectories[trial, step] = np.random.choice(choices) + trajectories[trial, step - 1]

    expected_value = np.mean(trajectories[:, -1])
    variance = np.var(trajectories[:, -1])
    return trajectories, expected_value, variance


def update(i, lines, trajectories):
    for trajectory, line in zip(trajectories, lines):
        line.set_data(range(i+1), trajectory[:i+1])


def plot_animation(trajectories):
    fig, ax = plt.subplots()
    ax.set(xlim=(0, 100), xlabel='X')
    ax.set(ylim=(-50, 50), ylabel='Y')
    lines = [ax.plot([], [])[0] for _ in trajectories]
    _ = animation.FuncAnimation(fig, update, trajectories.shape[1], fargs=(lines, trajectories), interval=50, repeat=False)
    plt.show()


def main():
    trajectories, expected_value, variance = random_walk()
    print(f"期待値は{expected_value}")
    print(f"分散は{variance}")
    plot_animation(trajectories)


if __name__ == '__main__':
    main()
