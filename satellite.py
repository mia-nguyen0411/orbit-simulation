import numpy as np


class Satellite:
    def __init__(self):
        EARTH_RADIUS = 6.371e6 # Set the radius of the earth for altitude calculations
        self.position = np.array([EARTH_RADIUS + 4e5, 0.0])  # Initial position x and y
        self.velocity = np.array([0.0, 7670.0]) # Set initial velocity for a satellite
        self.trail = [] # list to store the satellite's trail for visualisation
        self.altitude_history = [] # list to store altitude history for visualisation
        

    # Update the satellite's velocity and position based on the gravitational force from the earth and the time step dt from the self and dt parameters
    def update(self, dt):
        MU = 3.986e14 # Standard gravitational parameter for Earth (m^3/s^2)

        r = -self.position # Vector from satellite to earth
        distance = np.linalg.norm(r) # Distance from satellite to earth
        direction = r / distance # unit vector from satellite to earth

        acceleration = direction * (MU / distance**2) # calculate acceleration due to gravity

        self.velocity += acceleration * dt #Update velocity from acceleration and dt values
        self.position += self.velocity * dt # Update position from velocity and dt values

        # update the trail
        self.trail.append(self.position.copy()) # Add current satellite position to the trail

        if len(self.trail) > 500: #Limit the trail length to 500 points
            self.trail.pop(0) # Remove the oldest point from the trail to maintain the length

        # calculate altitude and store it in the history
        altitude = np.linalg.norm(self.position) # Calculate altitude as the distance from the earth's center
        self.altitude_history.append(altitude) # Add the current altitude to the history

        if len(self.altitude_history) > 300: # limit the altitude history length to 300 points
            self.altitude_history.pop(0) # Remove the oldest altitude from the history to maintain the length
        
