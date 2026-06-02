import pygame
from typing import List, Tuple

def update_simulation(dt: float, simulation_speed: float, zoom: float, camera_x: float, camera_y: float, scale: float, satellite, mars, moon, asteroids: List) -> tuple[float, float]:
    simulation_dt = dt * simulation_speed
    keys = pygame.key.get_pressed()

    camera_speed_world = 300 / (scale * zoom)
    velocity_step = 6.0 * dt

    if keys[pygame.K_UP]:
        satellite.velocity[1] += velocity_step
    if keys[pygame.K_DOWN]:
        satellite.velocity[1] -= velocity_step

    if keys[pygame.K_a]:
        camera_x += camera_speed_world * dt
    if keys[pygame.K_d]:
        camera_x -= camera_speed_world * dt
    if keys[pygame.K_w]:
        camera_y += camera_speed_world * dt
    if keys[pygame.K_s]:
        camera_y -= camera_speed_world * dt

    satellite.update(simulation_dt)
    mars.update(simulation_dt)
    moon.update(simulation_dt)

    for asteroid in asteroids:
        asteroid.update(simulation_dt)

    return camera_x, camera_y

def compute_status_and_texts(satellite) -> tuple[str, List[str]]:
    speed = (satellite.velocity[0] ** 2 + satellite.velocity[1] ** 2) ** 0.5
    altitude = (satellite.position[0] ** 2 + satellite.position[1] ** 2) ** 0.5

    texts = [
        f"Altitude: {altitude:.2f} units",
        f"Speed: {speed:.2f} units/s",
        f"VX: {satellite.velocity[0]:.2f} units/s",
        f"VY: {satellite.velocity[1]:.2f} units/s",
    ]

    status = "STABLE ORBIT"
    if altitude < (50 * 4e5 + 6.371e6):
        status = "RE-ENTRY WARNING"
    if altitude > (5 * 4e5 + 6.371e6):
        status = "ESCAPE TRAJECTORY WARNING"

    return texts, status