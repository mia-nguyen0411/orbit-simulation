import pygame
from satellite import Satellite

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

satellite = Satellite()

#define center to draw orbit view for centered earth
center = (400, 400)

def to_screen(position):
    scale = 2 # scale factor to convert from simulation units to screen pixels
    return ((int(center[0]) + position[0] * scale), 
            (int(center[1] + position[1] * scale)))

pygame.draw.circle(screen, (0, 100, 255), center, 20) # Draw Earth
#pygame.draw.circle(screen, (255, 255, 255), to_screen(satellite.position), 5)
    
    