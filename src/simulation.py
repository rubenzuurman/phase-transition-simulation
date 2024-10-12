import numpy as np
import pygame

class Simulation:
    
    def __init__(self, width, height, number_of_particles, particle_radius, position, force_magnitude, enable_borders):
        # Set members variables.
        self.width = width
        self.height = height
        self.number_of_particles = number_of_particles
        self.particle_radius = particle_radius
        self.position = position
        self.force_magnitude = force_magnitude
        self.enable_borders = enable_borders
        
        # Precalculate particle surface area.
        self.particle_surf_area = particle_radius * particle_radius * np.pi
        
        # Initialize list of particle positions and velocities.
        self.particle_positions_x = (np.random.rand(number_of_particles) * self.width) - (self.width / 2)
        self.particle_positions_y = (np.random.rand(number_of_particles) * self.width) - (self.width / 2)
        self.particle_velocities_x = np.zeros(number_of_particles)
        self.particle_velocities_y = np.zeros(number_of_particles)
        
        # Store particle starting positions for the calculation of the diffusion coefficient.
        self.particle_starting_positions = [(x, y) for x, y in zip(self.particle_positions_x, self.particle_positions_y)]
        self.diffusion_coefficient = 0
        
        # Simulation time tracker.
        self.time = 0
    
    def update(self, delta):
        # Calculate acceleration magnitude.
        acceleration_magnitude = self.force_magnitude / self.particle_surf_area
        
        # Generate list of random angles.
        acceleration_thetas = np.random.rand(self.number_of_particles) * np.pi * 2
        
        # Generate normalized vectors in random directions, also multiplied by delta_time.
        acceleration_x = np.cos(acceleration_thetas) * acceleration_magnitude * delta
        acceleration_y = np.sin(acceleration_thetas) * acceleration_magnitude * delta
        
        # Add accelerations to velocities and velocities to positions.
        self.particle_velocities_x = np.add(self.particle_velocities_x, acceleration_x)
        new_particle_positions_x = np.add(self.particle_positions_x, self.particle_velocities_x * delta)
        self.particle_velocities_y = np.add(self.particle_velocities_y, acceleration_y)
        new_particle_positions_y = np.add(self.particle_positions_y, self.particle_velocities_y * delta)
        
        # Check collisions with walls.
        if self.enable_borders:
            for index, (new_particle_x, new_particle_y) in enumerate(zip(new_particle_positions_x, new_particle_positions_y)):
                old_position = (self.particle_positions_x[index], self.particle_positions_y[index])
                new_position = (new_particle_x, new_particle_y)
                
                # Check left wall collision.
                if new_particle_x < -self.width / 2:
                    m, b = get_line_equation(p1=old_position, p2=new_position)
                    left_wall_intersect_y = m * (-self.width / 2) + b
                    if left_wall_intersect_y < -self.height / 2:
                        # Intersection with bottom wall instead.
                        self.particle_velocities_y[index] *= -1
                    elif left_wall_intersect_y > self.height / 2:
                        # Intersection with top wall instead.
                        self.particle_velocities_y[index] *= -1
                    else:
                        # Intersection with left wall.
                        self.particle_velocities_x[index] *= -1
                
                # Check right wall collision.
                if new_particle_x > self.width / 2:
                    m, b = get_line_equation(p1=old_position, p2=new_position)
                    right_wall_intersect_y = m * (self.width / 2) + b
                    if right_wall_intersect_y < -self.height / 2:
                        # Intersection with bottom wall instead.
                        self.particle_velocities_y[index] *= -1
                    elif right_wall_intersect_y > self.height / 2:
                        # Intersection with top wall instead.
                        self.particle_velocities_y[index] *= -1
                    else:
                        # Intersection with right wall.
                        self.particle_velocities_x[index] *= -1
                
                # Check bottom wall collision.
                if new_particle_y < -self.height / 2:
                    m, b = get_line_equation(p1=old_position, p2=new_position)
                    bottom_wall_intersect_x = ((-self.height / 2) - b) / m
                    if bottom_wall_intersect_x < -self.width / 2:
                        # Intersection with left wall instead.
                        self.particle_velocities_x[index] *= -1
                    elif bottom_wall_intersect_x > self.width / 2:
                        # Intersection with right wall instead.
                        self.particle_velocities_x[index] *= -1
                    else:
                        # Intersect with bottom wall.
                        self.particle_velocities_y[index] *= -1
                
                # Check top wall collision.
                if new_particle_y > self.height / 2:
                    m, b = get_line_equation(p1=old_position, p2=new_position)
                    top_wall_intersect_x = ((self.height / 2) - b) / m
                    if top_wall_intersect_x < -self.width / 2:
                        # Intersection with left wall instead.
                        self.particle_velocities_x[index] *= -1
                    elif top_wall_intersect_x > self.width / 2:
                        # Intersection with right wall instead.
                        self.particle_velocities_x[index] *= -1
                    else:
                        # Intersect with top wall.
                        self.particle_velocities_y[index] *= -1
        
        # Add the final particle velocities to the particle positions.
        self.particle_positions_x = np.add(self.particle_positions_x, self.particle_velocities_x * delta)
        self.particle_positions_y = np.add(self.particle_positions_y, self.particle_velocities_y * delta)
        
        # Increment simulation time after updating particle positions.
        self.time += delta
        
        # Calculate diffusion coefficient from current positions and starting positions.
        particle_current_positions = [(x, y) for x, y in zip(self.particle_positions_x, self.particle_positions_y)]
        mean_R_squared = sum([(end[0] - start[0]) * (end[0] - start[0]) + (end[1] - start[1]) * (end[0] - start[0]) for start, end in zip(self.particle_starting_positions, particle_current_positions)]) / self.number_of_particles
        self.diffusion_coefficient = mean_R_squared / (4 * self.time)
    
    def render(self, display, font_dict, camera, resolution):
        # Get camera position to avoid calling this function number_of_particles times.
        camera_position = camera.get_position()
        
        # Calculate corner positions.
        screen_topleft_x = (resolution[0] / 2) + (self.position[0] - (self.width / 2) - camera_position[0]) * camera.get_zoom()
        screen_topleft_y = (resolution[1] / 2) + (self.position[1] - (self.height / 2) - camera_position[1]) * camera.get_zoom()
        
        screen_topright_x = (resolution[0] / 2) + (self.position[0] + (self.width / 2) - camera_position[0]) * camera.get_zoom()
        screen_topright_y = (resolution[1] / 2) + (self.position[1] - (self.height / 2) - camera_position[1]) * camera.get_zoom()
        
        screen_bottomleft_x = (resolution[0] / 2) + (self.position[0] - (self.width / 2) - camera_position[0]) * camera.get_zoom()
        screen_bottomleft_y = (resolution[1] / 2) + (self.position[1] + (self.height / 2) - camera_position[1]) * camera.get_zoom()
        
        screen_bottomright_x = (resolution[0] / 2) + (self.position[0] + (self.width / 2) - camera_position[0]) * camera.get_zoom()
        screen_bottomright_y = (resolution[1] / 2) + (self.position[1] + (self.height / 2) - camera_position[1]) * camera.get_zoom()
        
        # Render walls.
        if self.enable_borders:
            pygame.draw.line(display, (255, 0, 0), (screen_topleft_x, screen_topleft_y), (screen_topright_x, screen_topright_y), 1)
            pygame.draw.line(display, (255, 0, 0), (screen_topright_x, screen_topright_y), (screen_bottomright_x, screen_bottomright_y), 1)
            pygame.draw.line(display, (255, 0, 0), (screen_bottomright_x, screen_bottomright_y), (screen_bottomleft_x, screen_bottomleft_y), 1)
            pygame.draw.line(display, (255, 0, 0), (screen_bottomleft_x, screen_bottomleft_y), (screen_topleft_x, screen_topleft_y), 1)
        
        # Render particles.
        for particle_position in zip(self.particle_positions_x, self.particle_positions_y):
            screen_x = (resolution[0] / 2) + (self.position[0] + particle_position[0] - camera_position[0]) * camera.get_zoom()
            screen_y = (resolution[1] / 2) + (-self.position[1] + particle_position[1] - camera_position[1]) * camera.get_zoom()
            radius = self.particle_radius * camera.get_zoom()
            # TODO: If radius is less than 0.5, use set_at instead.
            if radius < 2:
                radius = 2
            pygame.draw.circle(display, (255, 255, 255), (screen_x, screen_y), radius, width=1)
        
        # Get suitable text height. The height of the text should be less than 0.02*sim_height.
        # If the smallest font size is still too big, don't render the text at all.
        selected_font = None
        font_render_height = None
        for font_size, font in reversed(font_dict.items()):
            if font.get_rect("1").height <= 0.02 * self.height * camera.get_zoom():
                selected_font = font
                font_render_height = font.get_rect("1").height
                break
        
        # Render properties of the simulation.
        if not (selected_font is None):
            render_text(display, selected_font, f"Number of particles: {self.number_of_particles}", (0, 255, 0), (screen_topleft_x + font_render_height, screen_topleft_y + font_render_height))
            render_text(display, selected_font, f"Diffusion coefficient: {self.diffusion_coefficient:.2f}", (0, 255, 0), (screen_topleft_x + font_render_height, screen_topleft_y + font_render_height * 3))

def get_line_equation(p1, p2):
    m = (p1[1] - p2[1]) / (p1[0] - p2[0])
    b = p1[1] - m * p1[0]
    return m, b

def render_text(display, font, text, color, position):
    font.render_to(display, position, text, color)
