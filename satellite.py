import numpy as np

class Satellite:
    def __init__(self):
        self.position = np.array([200.0, 0.0])  # Initial position x and y
        self.velocity = np.array([0.0, 1.2]) # Set initial velocity for a satellite
        self.G = 2000 # set gravitational constant
        self.trail = [] # list to store the satellite's trail for visualisation

    # Update the satellite's velocity and position based on the gravitational force from the earth and the time step dt from the self and dt parameters
    def update(self, dt):
        r = -self.position # Vector from satellite to earth
        distance = np.linalg.norm(r) # Distance from satellite to earth
        direction = r / distance # unit vector from satellite to earth

        acceleration = direction * (self.G / distance**2) # calculate acceleration due to gravity

        self.velocity += acceleration * dt #Update velocity from acceleration and dt values
        self.position += self.velocity * dt # Update position from velocity and dt values

        # update the trail
        self.trail.append(self.position.copy()) # Add current satellite position to the trail

        if len(self.trail) > 500: #Limit the trail length to 500 points
            self.trail.pop(0) # Remove the oldest point from the trail to maintain the length
        
