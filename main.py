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
status = "STABLE ORBIT"

if altitude < 50:
    status = "RE-ENTRY WARNING"
if altitude > 5:
    status = "ESCAPE TRAJECTORY WARNING"

def to_screen(position):
    scale = 2  # scale factor to convert from simulation units to screen pixels
    return (int(center[0] + position[0] * scale),
            int(center[1] + position[1] * scale))

running = True
while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if keys[pygame.K_UP]:
            satellite.velocity[1] += 0.1  # Increase the y-component of velocity
        
        if keys[pygame.K_DOWN]:
            satellite.velocity[1] -= 0.1  # Decrease the y-component of velocity

    dt = clock.tick(60) / 1000.0  # seconds elapsed since last frame (capped at 60 fps)
    satellite.update(dt)

    screen.fill((0, 0, 0))  # Clear screen to black each frame

    pygame.draw.circle(screen, (0, 100, 255), center, 20)  # Draw Earth

    # function to print the text to the screen
    for i, t in enumerate(texts):
        text = font.render(t, True, (0, 255, 0))
        screen.blit(text, (10, 10 + i*20))    

    for p in satellite.trail:
        pygame.draw.circle(screen, (100, 150, 100), to_screen(p), 3)  # Draw trail

    pygame.draw.circle(screen, (255, 255, 255), to_screen(satellite.position), 5)  # Draw satellite
    status_text = font.render(status, True, (255, 0, 0))
    screen.blit(status_text, (500, 20))

    pygame.display.flip()

pygame.quit()

    