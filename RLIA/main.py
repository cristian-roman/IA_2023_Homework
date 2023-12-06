import numpy as np
from Environment import Environment
from QLearn import QLearn

if __name__ == "__main__":
    env = Environment()
    q_learn = QLearn()
    q_learn.learn(env)
    q_learn.display_actions(env)
