class Environment:

    def __init__(self):
        self.start = (0, 3)
        self.goal = (7, 3)
        self.wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
        self.size = (10, 7)
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def step(self, state, action):
        state_x = state[0]
        state_y = state[1]

        next_state_x = state_x + self.actions[action][0]
        next_state_y = state_y + self.actions[action][1]

        if next_state_x < 0:
            next_state_x = 0
        elif next_state_x >= self.size[0]:
            next_state_x = self.size[0] - 1

        next_state_y -= self.wind[next_state_x]
        if next_state_y < 0:
            next_state_y = 0
        elif next_state_y >= self.size[1]:
            next_state_y = self.size[1] - 1

        next_state = (next_state_x, next_state_y)

        if next_state == self.goal:
            reward = 100000
            done = True
        else:
            reward = -1
            done = False

        return next_state, reward, done

