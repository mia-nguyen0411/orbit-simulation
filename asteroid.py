import numpy as np
import random

class Asteroid:
    def __init__(self):
        self.orbit_radius = random.randint(1e6, 1e7)
        self.angle = random.uniform(0, 2 * np.pi)
        self.speed = random.uniform(1e3, 1e4)
        self.size = random.randint(10, 30)

    def update(self, dt):
        self.angle += self.speed * dt 
    
    def get_position(self):
        x = np.cos(self.angle) * self.orbit_radius
        y = np.sin(self.angle) * self.orbit_radius

        return  np.array([x, y])