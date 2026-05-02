import numpy as np

class Satellite:
    def _init(self):
        self.position = np.array([200.0, 0.0])  # Initial position x and y
        self.velocity = np.array([0.0, 1.2]) # Set initial velocity for a satellite
        self.G = 2000 # set gravitational constant

    # Update the satellite's velocity and position based on the gravitational force from the earth and the time step dt from the self and dt parameters
    def update(self, dt):
        r = -self.position # Vector from satellite to earth
        distance = np.linalg.norm(r) # Distance from satellite to earth
        direction = r / distance # unit vector from satellite to earth

        acceleration = direction * (self.G / distance**2) # calculate acceleration due to gravity

        self.velocity += acceleration * dt #Update velocity from acceleration and dt values
        self.position += self.velocity * dt # Update position from velocity and dt values