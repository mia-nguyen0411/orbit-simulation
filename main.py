import pygame
from satellite import Satellite
from planet import Planet
from asteroid import Asteroid
import random

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
star = [(random.randint(0,980), random.randint(0, 1223)) for _ in range(120)]

scale = 4e-5
simulation_speed = 5.0 # increase to speed up the simulation

zoom = 1.0
camera_x = 0
camera_y = 0
MIN_ZOOM = 0.2
MAX_ZOOM = 20.0

satellite = Satellite()

mars = Planet(
    orbit_radius = (300 / scale),
    size = 8,
    color = (200, 100, 50),
    speed = 0.2
)

moon = Planet(
    orbit_radius = (150 / scale),
    size = 5,
    color = (180, 180, 180),
    speed = 0.5
)

asteroids =[]

for _ in range (300):
    asteroids.append(Asteroid(scale))

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

if altitude < (50*4e5 + 6.371e6):
    status = "RE-ENTRY WARNING"
if altitude > (5*4e5 + 6.371e6):
    status = "ESCAPE TRAJECTORY WARNING"

def to_screen(position):
    current_scale = scale * zoom  # apply zoom as a multiplier to the base simulation scale
    return (int(center[0] + (position[0] + camera_x) * current_scale),
            int(center[1] + (position[1] + camera_y) * current_scale))

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:

            if event.y > 0:
                zoom *= 1.1

            if event.y < 0:
                zoom *= 0.9

            zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom))

    dt = clock.tick(60) / 1000.0  # seconds elapsed since last frame (capped at 60 fps)
    simulation_dt = dt * simulation_speed

    keys = pygame.key.get_pressed()

    # Keep keyboard controls frame-based and convert pan speed from px/s to world units.
    camera_speed_world = 300 / (scale * zoom)
    velocity_step = 6.0 * dt

    if keys[pygame.K_UP]:
        satellite.velocity[1] += velocity_step  # Increase the y-component of velocity
    if keys[pygame.K_DOWN]:
        satellite.velocity[1] -= velocity_step  # Decrease the y-component of velocity

    if keys[pygame.K_a]:
        camera_x += camera_speed_world * dt  # Move camera left
    if keys[pygame.K_d]:
        camera_x -= camera_speed_world * dt  # Move camera right
    if keys[pygame.K_w]:
        camera_y += camera_speed_world * dt  # Move camera up
    if keys[pygame.K_s]:
        camera_y -= camera_speed_world * dt  # Move camera down

    satellite.update(simulation_dt)

    mars.update(simulation_dt)
    moon.update(simulation_dt)

    for asteroid in asteroids:
        asteroid.update(simulation_dt)

    screen.fill((5, 5, 15))  # Clear screen to black each frame

    for s in star:
        pygame.draw.circle(screen, (255, 255, 255), s, 1)

    pygame.draw.circle(screen, (0, 100, 255), center, 20)  # Draw Earth
    
    # define new planet position
    mars_position = to_screen(mars.get_position())
    moon_position = to_screen(moon.get_position())

    # draw planets
    pygame.draw.circle(screen, mars.color, mars_position, mars.size)
    pygame.draw.circle(screen, moon.color, moon_position, moon.size)

    # draw orbit rings
    pygame.draw.circle(screen, (50, 50, 50), center, max(1, int(300 * zoom)), 1)
    pygame.draw.circle(screen, (50, 50, 50), center, max(1, int(150 * zoom)), 1)

    # mars text
    mars_text = font.render("Mars", True, (255, 255, 255))

    # draw asteroids
    for asteroid in asteroids:
        position = to_screen(asteroid.get_position())
        pygame.draw.circle(screen, (150, 150, 150), position, asteroid.size)

    # function to print the text to the screen
    for i, t in enumerate(texts):
        text = font.render(t, True, (0, 255, 0))
        screen.blit(text, (10, 10 + i*20))    

    # zoom text
    zoom_text = font.render(f"Zoom: {zoom:.2f}x", True, (255, 255, 0))
    
    #simulation status text
    simulation_status = font.render(f"Simulation speed: {simulation_speed:.1f}x", True, (255, 255, 0))

    # Draw trail as connected line instead of individual circles
    if len(satellite.trail) > 1:
        trail_points = [to_screen(p) for p in satellite.trail]
        pygame.draw.lines(screen, (100, 150, 100), False, trail_points, 1)

    for r in range(100, 400, 100):
        pygame.draw.circle(screen, (50, 50, 50), center, max(1, int(r * zoom)), 1) # draw  fried lines like radar

    pygame.draw.circle(screen, (255, 255, 255), to_screen(satellite.position), 5)  # Draw satellite
    draw_vector(screen, to_screen(satellite.position), satellite.velocity, scale=0.015)# Draw velocity vector
    draw_graph(screen, satellite.altitude_history, 500, 500, 250, 150)
    status_text = font.render(status, True, (255, 0, 0))
    screen.blit(mars_text, (mars_position[0]+10, mars_position[1]))
    screen.blit(status_text, (800, 20))
    screen.blit(zoom_text, (800, 40))
    screen.blit(simulation_status, (700, 60))

    pygame.display.flip()

pygame.quit()

    