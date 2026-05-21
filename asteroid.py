import numpy as np
import random

class Asteroid:
    def __init__(self, scale):
        self.orbit_radius = random.randint(int(350 / scale), int(500 / scale))
        self.angle = random.uniform(0, 2 * np.pi)
        self.speed = random.uniform(0.05, 0.2)
        self.size = random.randint(1, 4)

    def update(self, dt):
        self.angle += self.speed * dt 
    
    def get_position(self):
        x = np.cos(self.angle) * self.orbit_radius
        y = np.sin(self.angle) * self.orbit_radius

        return  np.array([x, y])