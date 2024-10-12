from src.simulation import Simulation
from src.window import show_window

def run():
    simulation = Simulation(width=1000, height=1000, number_of_particles=10, particle_radius=4, position=(-2000, 0), force_magnitude=10000, enable_borders=True)
    simulation2 = Simulation(width=1000, height=1000, number_of_particles=20, particle_radius=4, position=(-1000, 0), force_magnitude=10000, enable_borders=True)
    simulation3 = Simulation(width=1000, height=1000, number_of_particles=50, particle_radius=4, position=(0, 0), force_magnitude=10000, enable_borders=True)
    simulation4 = Simulation(width=1000, height=1000, number_of_particles=100, particle_radius=4, position=(1000, 0), force_magnitude=10000, enable_borders=True)
    simulation5 = Simulation(width=1000, height=1000, number_of_particles=500, particle_radius=4, position=(2000, 0), force_magnitude=10000, enable_borders=True)
    show_window(resolution=(1920, 1080), simulations=[simulation, simulation2, simulation3, simulation4, simulation5])
