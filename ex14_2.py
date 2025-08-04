import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import math


class Agent:
    def __init__(self, space_size):
        self.space_size = space_size
        self.x = random.uniform(0, space_size)
        self.y = random.uniform(0, space_size)
        self.status = 'health'
        self.infection_date = 0

    def move(self):
        self.x = (self.x + random.uniform(-1.0, 1.0)) % self.space_size
        self.y = (self.y + random.uniform(-1.0, 1.0)) % self.space_size

    def infect(self, agents, i):
        if self.status == 'health':
            for agent in agents:
                if agent.status == 'infected':
                    distance = math.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2)
                    if 0 < distance <= 3:
                        self.status = 'infected'
                        self.infection_date = i
        elif self.status == 'infected':
            if i - self.infection_date == 15:
                self.status = 'health'


def agent_simulation():
    loop_limit = 500
    agent_num = 100
    space_size = 50
    random.seed(1)
    output = np.empty((loop_limit, agent_num, 2))
    colors = []
    agents = [Agent(space_size) for _ in range(agent_num)]
    agents[0].status = 'infected'
    for j in range(loop_limit):
        color = []
        for i, agent in enumerate(agents):
            if agent.status == 'infected':
                color.append("red")
            elif agent.status == 'health':
                color.append("blue")
            output[j, i, 0] = agent.x
            output[j, i, 1] = agent.y
            agent.move()
            agent.infect(agents, j + 1)
        colors.append(color)

    return output, colors


def update(i, scatter, output, colors):
    scatter.set_offsets(output[i])
    scatter.set_color(colors[i])
    return scatter,


def main():
    output, colors = agent_simulation()
    fig, ax = plt.subplots()
    ax.set(xlim=(0, 50), ylim=(0, 50))
    scatter = ax.scatter([], [], s=10)
    anim = animation.FuncAnimation(fig, update, frames=len(output),
                                   fargs=(scatter, output, colors), interval=50, blit=True)
    plt.show()


if __name__ == '__main__':
    main()