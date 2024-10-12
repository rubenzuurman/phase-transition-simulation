import math

import pygame

from src.camera import Camera

# Root 2 is used very often, so this will save a bit of performance.
SQRT2 = math.sqrt(2)

# Used for zoom keys. Prevents zooming in/out many times when the up/down button is held down.
UP_RELEASED = True
DOWN_RELEASED = True

def show_window(resolution, simulations):
    # Init pygame.
    pygame.init()
    
    # Initialize font.
    font_dict = {n: pygame.freetype.SysFont("Courier New", n) for n in range(6, 18, 2)}
    
    # Create display.
    display = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Spontaneous Crystallization")
    
    # Initialize camera.
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
        
        # Update simulations and camera.
        for simulation in simulations:
            simulation.update(delta=0.01)
        camera.update(delta=0.01)
        
        # Clear display.
        display.fill("black")
        
        # Render simulations at their respective positions.
        for simulation in simulations:
            simulation.render(display, font_dict, camera, resolution)
        
        # Render debug text.
        render_text(display, font_dict[16], f"Camera position: ({camera.get_position()[0]:.2f}, {camera.get_position()[1]:.2f})", (255, 0, 0), (10, 10))
        render_text(display, font_dict[16], f"Camera velocity: ({camera.get_velocity()[0]:.2f}, {camera.get_velocity()[1]:.2f})", (255, 0, 0), (10, 30))
        render_text(display, font_dict[16], f"Camera zoom: {camera.get_zoom():.2f} (target: {camera.get_zoom_target():.2f})", (255, 0, 0), (10, 50))
        
        # Render frame and tick clock.
        pygame.display.flip()
        clock.tick(60)

def handle_inputs(keys_pressed, camera, delta):
    global UP_RELEASED, DOWN_RELEASED
    
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
    camera.set_velocity((camera_velocity_x, camera_velocity_y))
    
    # Handle camera zoom target.
    if keys_pressed[pygame.K_UP] and UP_RELEASED:
        camera.set_zoom_target(camera.get_zoom_target() * 2)
        UP_RELEASED = False
    if keys_pressed[pygame.K_DOWN] and DOWN_RELEASED:
        camera.set_zoom_target(camera.get_zoom_target() / 2)
        DOWN_RELEASED = False
    
    if not keys_pressed[pygame.K_UP]:
        UP_RELEASED = True
    if not keys_pressed[pygame.K_DOWN]:
        DOWN_RELEASED = True

def render_text(display, font, text, color, position):
    font.render_to(display, position, text, color)
