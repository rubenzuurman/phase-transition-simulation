import math

import pygame

from src.camera import Camera

# Root 2 is used very often, so this will save a bit of performance.
SQRT2 = math.sqrt(2)

def show_window(resolution, simulation):
    # Init pygame.
    pygame.init()
    
    # Create display.
    display = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Spontaneous Crystallization")
    
    camera = Camera()
    
    # Create clock and start main loop.
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Handle inputs.
        keys_pressed = pygame.key.get_pressed()
        handle_inputs(keys_pressed, camera, delta=0.01)
        
        # Update simulation.
        simulation.update(delta=0.01)
        
        # Clear display.
        display.fill("black")
        
        # Render simulation in the middle of the screen.
        simulation.render(display, camera, position=(resolution[0] / 2, resolution[1] / 2))
        
        # Render frame and tick clock.
        pygame.display.flip()
        clock.tick(60)

def handle_inputs(keys_pressed, camera, delta):
    # Get camera velocity in both directions.
    camera_velocity_x = 0
    camera_velocity_y = 0
    if keys_pressed[pygame.K_w]:
        camera_velocity_y -= 1
    if keys_pressed[pygame.K_a]:
        camera_velocity_x -= 1
    if keys_pressed[pygame.K_s]:
        camera_velocity_y += 1
    if keys_pressed[pygame.K_d]:
        camera_velocity_x += 1
    
    # Normalize camera velocity.
    camera_speed = 1000
    if camera_velocity_x != 0 and camera_velocity_y != 0:
        camera_velocity_x = camera_velocity_x / SQRT2
        camera_velocity_y = camera_velocity_y / SQRT2
    camera_velocity_x *= camera_speed
    camera_velocity_y *= camera_speed
    
    # Move camera.
    camera.move_by((camera_velocity_x * delta, camera_velocity_y * delta))
