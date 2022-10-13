

class Percept:
    def __init__(self, stench: bool, breeze: bool, glitter: bool, bump: bool, scream: bool, is_terminated: bool, reward: float):
        self.stench = stench
        self.breeze = breeze
        self.glitter = glitter
        self.bump = bump
        self.scream = scream
        self.is_terminated = is_terminated
        self.reward = reward

    def show(self):
        return f"stench:{self.stench} breeze:{self.breeze} glitter:{self.glitter} bump:{self.bump} scream:{self.scream} is_terminated:{self.is_terminated} reward:{self.reward}"