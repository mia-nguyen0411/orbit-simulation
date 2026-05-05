import pygame
from satellite import Satellite

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

satellite = Satellite()

#define center to draw orbit view for centered earth
center = (400, 400)

#create font with data to show
font = pygame.font.SysFont("consolas", 20)
speed = (satellite.velocity[0]**2 + satellite.velocity[1]**2)**0.5
altitude = (satellite.position[0]**2 + satellite.position[1]**2)**0.5

texts = [
    f"Altitude: {altitude:.2f} units",
    f"Speed: {speed: .2f} units/s",
    f"VX: {satellite.velocity[0]:.2f} units/s",
    f"VY: {satellite.velocity[1]:.2f} units/s"
]

# function to print the text to the screen
for i, t in enumerate(texts):
    text = font.render(t, True, (0, 255, 0))
    screen.blit(text, (10, 10 + i*20))

def to_screen(position):
    scale = 2  # scale factor to convert from simulation units to screen pixels
    return (int(center[0] + position[0] * scale),
            int(center[1] + position[1] * scale))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000.0  # seconds elapsed since last frame (capped at 60 fps)
    satellite.update(dt)

    screen.fill((0, 0, 0))  # Clear screen to black each frame

    pygame.draw.circle(screen, (0, 100, 255), center, 20)  # Draw Earth

    for p in satellite.trail:
        pygame.draw.circle(screen, (0, 150, 0), to_screen(p), 2)  # Draw trail

    pygame.draw.circle(screen, (255, 255, 255), to_screen(satellite.position), 5)  # Draw satellite

    pygame.display.flip()

pygame.quit()

    