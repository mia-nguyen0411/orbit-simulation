import numpy as np

class Planet:
    def __init__(self, orbit_radius, size, color, speed):
        self.orbit_radius = orbit_radius
        self.size = size
        self.color = color
        self.speed = speed

        self.angle = 0

    def update(self, dt):
        self.angle += self.speed * dt

    def get_position(self):
        x = np.cos(self.angle) * self.orbit_radius
        y = np.sin(self.angle) * self.orbit_radius

        return np.array([x, y])