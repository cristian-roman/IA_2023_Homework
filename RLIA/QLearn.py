import numpy as np
from Environment import Environment
import matplotlib.pyplot as plt


class QLearn:

    def __init__(self):
        self.q_table = -np.ones((10, 7, 4))
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_decay = 0.9
        self.episode_rewards = []

    def __get_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, 4)
        return np.argmax(self.q_table[state[0], state[1]])

    def __update(self, state, action, reward, next_state):
        current_q = self.q_table[state[0], state[1], action]
        next_max_q = np.max(self.q_table[next_state[0], next_state[1]])
        new_q = current_q + self.alpha * (reward + self.gamma * next_max_q - current_q)
        self.q_table[state[0], state[1], action] = new_q

    def learn(self, env: Environment):
        number_of_episodes = 1000
        for episode in range(number_of_episodes):
            state = env.start
            total_reward = 0

            while True:
                action = self.__get_action(state)
                next_state, reward, done = env.step(state, action)
                self.__update(state, action, reward, next_state)
                total_reward += reward
                state = next_state
                if state == env.goal:
                    break

            self.epsilon *= self.epsilon_decay
            self.epsilon = max(0.1, self.epsilon)

            self.episode_rewards.append(total_reward)

        self.__plot_rewards()

    def display_actions(self, env: Environment):
        state = env.start
        total_reward = 0
        done = False
        step = 1
        while not done:
            action = np.argmax(self.q_table[state[0], state[1]])

            print("Step: " + str(step) + " State: " + str(state) + " Action: " + self.__map_action(action))

            next_state, reward, done = env.step(state, action)
            step += 1
            total_reward += reward
            state = next_state

        print("Total reward: " + str(total_reward))

    def __plot_rewards(self):
        episodes = range(1, len(self.episode_rewards) + 1)
        plt.plot(episodes, self.episode_rewards, marker='o')
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.title('Episode Rewards during Learning')
        plt.show()

    @staticmethod
    def __map_action(action):
        if action == 0:
            return '←'
        elif action == 1:
            return '→'
        elif action == 2:
            return '↑'
        elif action == 3:
            return '↓'
        else:
            return ' '
