import pygame
from satellite import Satellite

pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

satellite = Satellite()

#define center to draw orbit view for centered earth
center = (450, 450)

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

# draw vector arrow
def draw_vector(screen, start, vector, scale=20):
    # Calculate the end point of the arrow based on the start point, vector and scale factor
    end = (
        int(start[0] + vector[0] * scale),
        int(start[1] + vector[1] * scale)
    )

    pygame.draw.line(screen, (255, 0, 0), start, end, 2) # Draw the arrow line
    pygame.draw.circle(screen, (255, 0, 0), end, 4) #Draw the arrow head as a circle at the end point

# draw altitude graph
def draw_graph(screen, data, x, y, width, height):
    if len(data) < 2:
        return # not enough data to draw graph
    
    max_value = max(data)
    min_value = min(data)

    points = []

    for i, value in enumerate(data): # Calculate the x and y coordinates for each data point in the graph
        px = x + (i / len(data)) * width # x coordinate based on index and total width

        normalised = (value - min_value) / (max_value - min_value + 1e-5) # normalise value to range [0, 1]

        py = y + height - normalised * height # y coordinate based on normalised value and total height

        points.append((px, py))
    
    pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height), 1) # Draw graph border

    pygame.draw.lines(screen, (0, 255, 0), False, points, 2) # Draw the graph line from points

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

    screen.fill((5, 5, 15))  # Clear screen to black each frame

    pygame.draw.circle(screen, (0, 100, 255), center, 20)  # Draw Earth

    # function to print the text to the screen
    for i, t in enumerate(texts):
        text = font.render(t, True, (0, 255, 0))
        screen.blit(text, (10, 10 + i*20))    

    for p in satellite.trail:
        pygame.draw.circle(screen, (100, 150, 100), to_screen(p), 3)  # Draw trail

    for r in range(100, 400, 100):
        pygame.draw.circle(screen, (50, 50, 50), center, r, 1) # draw  fried lines like radar

    pygame.draw.circle(screen, (255, 255, 255), to_screen(satellite.position), 5)  # Draw satellite
    draw_vector(screen, to_screen(satellite.position), satellite.velocity)# Draw velocity vector
    draw_graph(screen, satellite.altitude_history, 500, 500, 250, 150)
    status_text = font.render(status, True, (255, 0, 0))
    screen.blit(status_text, (600, 20))

    pygame.display.flip()

pygame.quit()

    