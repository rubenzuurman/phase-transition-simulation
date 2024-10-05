import numpy as np
import pygame

class Simulation:
    
    def __init__(self, width, height, number_of_particles, particle_radius):
        self.width = width
        self.height = height
        self.number_of_particles = number_of_particles
        self.particle_radius = particle_radius
        
        # Initialize list of particle positions.
        particles_x = (np.random.rand(number_of_particles) * self.width) - (self.width / 2)
        particles_y = (np.random.rand(number_of_particles) * self.width) - (self.width / 2)
        self.particle_positions = [[x, y] for x, y in zip(particles_x, particles_y)]
    
    def update(self, delta):
        pass
    
    def render(self, display, camera, position):
        # Get camera position to avoid calling this function number_of_particles times.
        camera_position = camera.get_position()
        
        # Render particles.
        for particle_position in self.particle_positions:
            screen_x = position[0] - camera_position[0] + particle_position[0]
            screen_y = position[1] - camera_position[1] + particle_position[1]
            pygame.draw.circle(display, (255, 255, 255), (screen_x, screen_y), self.particle_radius * 10, width=1)