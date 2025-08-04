import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class Agent:
    def __init__(self, space_size):
        self.space_size = space_size
        self.x = random.uniform(0, space_size)
        self.y = random.uniform(0, space_size)

    def move(self):
        self.x = (self.x + random.uniform(-1.0, 1.0)) % self.space_size
        self.y = (self.y + random.uniform(-1.0, 1.0)) % self.space_size


def agent_simulation():
    loop_limit = 500
    agent_num = 100
    space_size = 50
    random.seed(1)
    output = np.empty((loop_limit, agent_num, 2))
    agents = [Agent(space_size) for _ in range(agent_num)]
    for j in range(loop_limit):
        for i, agent in enumerate(agents):
            output[j, i, 0] = agent.x
            output[j, i, 1] = agent.y
            agent.move()

    return output


def update(i, scatter, output):
    scatter.set_offsets(output[i])
    return scatter,


def main():
    output = agent_simulation()
    fig, ax = plt.subplots()
    ax.set(xlim=(0, 50), ylim=(0, 50))
    scatter = ax.scatter([], [], s=10)
    anim = animation.FuncAnimation(fig, update, frames=len(output),
                                   fargs=(scatter, output), interval=50, blit=True)
    plt.show()


if __name__ == '__main__':
    main()