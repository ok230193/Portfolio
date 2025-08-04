import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.animation as animation


def random_walk_3d():
    trials = 200
    steps = 100
    trajectories = np.zeros((trials, steps, 3))
    random.seed(0)
    choices = [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1]]

    for trial in range(trials):
        for step in range(1, steps):
            trajectories[trial, step] = random.choices(choices) + trajectories[trial, step-1]

    zero_flag = np.zeros(trials)
    for idx in range(trials):
        if np.any(np.all(trajectories[idx, 1:] == 0, axis=1)):
            zero_flag[idx] = 1

    return_probability = np.mean(zero_flag) * 100.0
    return trajectories, return_probability



def update(i, lines, trajectories):
    for trajectory, line in zip(trajectories, lines):
        line.set_data_3d(trajectory[:i].T)


def plot_animation(trajectories):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set(xlim=(-20, 20), xlabel='X')
    ax.set(ylim=(-20, 20), ylabel='Y')
    ax.set(zlim=(-20, 20), zlabel='Z')
    lines = [ax.plot3D([], [], [])[0] for _ in trajectories]
    _ = animation.FuncAnimation(fig, update, trajectories.shape[1], fargs=(lines, trajectories), interval=50, repeat=False)
    plt.show()


def main():
    trajectories, return_probability = random_walk_3d()
    print(f"軌跡が原点に戻る確率は{return_probability}パーセント")
    plot_animation(trajectories)


if __name__ == '__main__':
    main()
