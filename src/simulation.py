import numpy as np
import pygame

class Simulation:
    
    def __init__(self, width, height, number_of_particles, particle_radius, position):
        self.width = width
        self.height = height
        self.number_of_particles = number_of_particles
        self.particle_radius = particle_radius
        self.position = position
        
        # Initialize list of particle positions.
        particles_x = (np.random.rand(number_of_particles) * self.width) - (self.width / 2)
        particles_y = (np.random.rand(number_of_particles) * self.width) - (self.width / 2)
        self.particle_positions = [[x, y] for x, y in zip(particles_x, particles_y)]
    
    def update(self, delta):
        pass
    
    def render(self, display, camera, resolution):
        # Get camera position to avoid calling this function number_of_particles times.
        camera_position = camera.get_position()
        
        # Render particles.
        for particle_position in self.particle_positions:
            screen_x = (resolution[0] / 2) + (self.position[0] + particle_position[0] - camera_position[0]) * camera.get_zoom()
            screen_y = (resolution[1] / 2) + (-self.position[1] + particle_position[1] - camera_position[1]) * camera.get_zoom()
            radius = self.particle_radius * camera.get_zoom()
            # TODO: If radius is less than 0.5, use set_at instead.
            if radius < 2:
                radius = 2
            pygame.draw.circle(display, (255, 255, 255), (screen_x, screen_y), radius, width=1)
