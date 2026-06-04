import pygame
from satellite import Satellite
from planet import Planet
from asteroid import Asteroid
from simulation import update_simulation, compute_status_and_texts
import random

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
star = [(random.randint(0,980), random.randint(0, 1223)) for _ in range(120)]

scale = 4e-5
simulation_speed = 5.0
default_speed = 3.0

zoom = 1.0
default_zoom = 1.0
MIN_ZOOM = 0.2
MAX_ZOOM = 20.0

camera_x = 0
camera_y = 0


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

#reset button
BUTTON_WIDTH = 210
BUTTON_HEIGHT = 42
BUTTON_MARGIN_X = 20
BUTTON_MARGIN_Y = 800
reset_button_shape = pygame.Rect(
    screen.get_width() - BUTTON_WIDTH - BUTTON_MARGIN_X,
    BUTTON_MARGIN_Y,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

button_font = pygame.font.SysFont("bahnschrift", 18, bold=True)

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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if reset_button_shape.collidepoint(event.pos):
                zoom = default_zoom
                simulation_speed = default_speed


        if event.type == pygame.MOUSEWHEEL:

            if event.y > 0:
                zoom *= 1.1

            if event.y < 0:
                zoom *= 0.9

            zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom))

    dt = clock.tick(60) / 1000.0  # seconds elapsed since last frame (capped at 60 fps)

    camera_x, camera_y = update_simulation(dt, simulation_speed, zoom, camera_x, camera_y, scale, satellite, mars, moon, asteroids)
    texts, status = compute_status_and_texts(satellite)

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

    mouse_position = pygame.mouse.get_pos()
    is_hovering_reset = reset_button_shape.collidepoint(mouse_position)
    
    # NASA-inspired mission-control button styling.
    base_color = (25, 33, 42) if is_hovering_reset else (18, 25, 34)
    frame_color = (90, 130, 160) if is_hovering_reset else (70, 105, 130)
    accent_color = (0, 210, 255) if is_hovering_reset else (0, 165, 215)
    text_color = (245, 250, 255)

    pygame.draw.rect(screen, base_color, reset_button_shape, border_radius=4)
    pygame.draw.rect(screen, frame_color, reset_button_shape, 2, border_radius=4)

    # Corner accents emulate instrument panel framing.
    x, y, w, h = reset_button_shape
    corner_len = 12
    pygame.draw.line(screen, accent_color, (x + 1, y + 1), (x + 1 + corner_len, y + 1), 2)
    pygame.draw.line(screen, accent_color, (x + 1, y + 1), (x + 1, y + 1 + corner_len), 2)
    pygame.draw.line(screen, accent_color, (x + w - 2, y + 1), (x + w - 2 - corner_len, y + 1), 2)
    pygame.draw.line(screen, accent_color, (x + w - 2, y + 1), (x + w - 2, y + 1 + corner_len), 2)
    pygame.draw.line(screen, accent_color, (x + 1, y + h - 2), (x + 1 + corner_len, y + h - 2), 2)
    pygame.draw.line(screen, accent_color, (x + 1, y + h - 2), (x + 1, y + h - 2 - corner_len), 2)
    pygame.draw.line(screen, accent_color, (x + w - 2, y + h - 2), (x + w - 2 - corner_len, y + h - 2), 2)
    pygame.draw.line(screen, accent_color, (x + w - 2, y + h - 2), (x + w - 2, y + h - 2 - corner_len), 2)

    # Small status indicator for a cockpit-style visual cue.
    indicator_color = (72, 255, 110) if is_hovering_reset else (200, 95, 70)
    pygame.draw.circle(screen, indicator_color, (x + 14, y + h // 2), 5)

    reset_button_text = button_font.render("RESET ZOOM", True, text_color)
    text_rect = reset_button_text.get_rect(center=reset_button_shape.center)
    text_rect.x += 8
    screen.blit(reset_button_text, text_rect)


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
    screen.blit(status_text, (700, 60))

    pygame.display.flip()

pygame.quit()

    