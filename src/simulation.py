import math

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
        
        # Calculate acceleration magnitude.
        acceleration_magnitude = self.force_magnitude / self.particle_surf_area
        
        # Predefine list of possible accelerations.
        self.possible_accelerations = [[acceleration_magnitude, 0], [-acceleration_magnitude, 0], [0, acceleration_magnitude], [0, -acceleration_magnitude]]
        
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
        # Get list of random indices of the acceleration options list.
        acceleration_vector_indices = np.random.choice([0, 1, 2, 3], size=self.number_of_particles)
        
        # Get x and y components from the acceleration vector indices list.
        acceleration_x = [self.possible_accelerations[acc_index][0] for acc_index in acceleration_vector_indices]
        acceleration_y = [self.possible_accelerations[acc_index][1] for acc_index in acceleration_vector_indices]
        
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
                left_wall = [(-self.width / 2, -self.height / 2), (-self.width / 2, self.height / 2)]
                if check_two_lines_intersect(l1=left_wall, l2=[old_position, new_position]):
                    self.particle_velocities_x[index] *= -1
                
                # Check right wall collision.
                right_wall = [(self.width / 2, -self.height / 2), (self.width / 2, self.height / 2)]
                if check_two_lines_intersect(l1=right_wall, l2=[old_position, new_position]):
                    self.particle_velocities_x[index] *= -1
                
                # Check bottom wall collision.
                bottom_wall = [(-self.width / 2, -self.height / 2), (self.width / 2, -self.height / 2)]
                if check_two_lines_intersect(l1=bottom_wall, l2=[old_position, new_position]):
                    self.particle_velocities_y[index] *= -1
                
                # Check top wall collision.
                top_wall = [(-self.width / 2, self.height / 2), (self.width / 2, self.height / 2)]
                if check_two_lines_intersect(l1=top_wall, l2=[old_position, new_position]):
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

def check_two_lines_intersect(l1, l2):
    """
    Expects l1 and l2 to be 1D lists containing two pairs each, one for the start of the line and one for the end of the line.
    Example: l1=[(start_x, start_y), (end_x, end_y)], l2=[(start_x, start_y), (end_x, end_y)]
    Returns a boolean indicating whether or not there has been an intersection.
    """
    # Get start and end points from lines.
    l1_start, l1_end = l1
    l2_start, l2_end = l2
    
    # Calculate coordinate transformation matrix from the angle of l1.
    l1_angle = math.atan2(l1_end[1] - l1_start[1], l1_end[0] - l1_start[0])
    rotation_angle = math.pi / 2 - l1_angle
    rotation_matrix = np.array([[math.cos(rotation_angle), -math.sin(rotation_angle)], [math.sin(rotation_angle), math.cos(rotation_angle)]])
    
    # Apply coordinate transformation to both l1 and l2 such that l1 is vertical.
    l1_start_rot = np.dot(rotation_matrix, l1_start)
    l1_end_rot = np.dot(rotation_matrix, l1_end)
    l2_start_rot = np.dot(rotation_matrix, l2_start)
    l2_end_rot = np.dot(rotation_matrix, l2_end)
    
    # If l2 is vertical, then no intersection exists unless l1_start_x==l2_start_x and (l2_start_y in range of l1 y or l2_end_y in range of l1 y) OR (l1_start_y in range of l2 y or l1_end_y in range of l2 y).
    if l2_start_rot[0] == l2_end_rot[0]:
        # Not the same x coordinate -> return False.
        if not (l1_start_rot[0] == l2_start_rot[0]):
            return False
        
        # Check if either l2_start or l2_end is within the y range of l1.
        l1_min_y = min(l1_start_rot[1], l1_end_rot[1])
        l1_max_y = max(l1_start_rot[1], l1_end_rot[1])
        l2_start_in_y_range = l2_start_rot[1] >= l1_min_y and l2_start_rot[1] <= l1_max_y
        l2_end_in_y_range   = l2_end_rot[1] >= l1_min_y and l2_end_rot[1] <= l1_max_y
        
        # Check if either l1_start of l1_end is within the y_range of l2.
        l2_min_y = min(l2_start_rot[1], l2_end_rot[1])
        l2_max_y = max(l2_start_rot[1], l2_end_rot[1])
        l1_start_in_y_range = l1_start_rot[1] >= l2_min_y and l1_start_rot[1] <= l2_max_y
        l1_end_in_y_range   = l1_end_rot[1] >= l2_min_y and l1_end_rot[1] <= l2_max_y
        
        # Return true if either start or end of either line is inside the other one.
        return l2_start_in_y_range or l2_end_in_y_range or l1_start_in_y_range or l1_end_in_y_range
    
    # Check if the start of l2 and the end of l2 are on opposite sides of l1 (note: l1 is vertical after the rotation).
    l2_start_left = l1_start_rot[0] - l2_start_rot[0] > 0
    l2_end_left = l1_start_rot[0] - l2_end_rot[0] > 0
    if l2_start_left == l2_end_left:
        return False
    
    # Get equation for l2.
    m, b = get_line_equation(l2_start_rot, l2_end_rot)
    
    # Plug in the x coordinate of l1 (don't have to worry about m being infinite since the case where l2 is vertical is already checked).
    y_intersect = m * l1_start_rot[0] + b
    
    # Check if the y coordinate of the intersection is in the y range of l1 (same as with vertical line, but single point).
    l1_min_y = min(l1_start_rot[1], l1_end_rot[1])
    l1_max_y = max(l1_start_rot[1], l1_end_rot[1])
    return y_intersect >= l1_min_y and y_intersect <= l1_max_y

def get_line_equation(p1, p2):
    if p1[0] == p2[0]:
        m = np.inf
    else:
        m = (p1[1] - p2[1]) / (p1[0] - p2[0])
    b = p1[1] - m * p1[0]
    return m, b

def render_text(display, font, text, color, position):
    font.render_to(display, position, text, color)
