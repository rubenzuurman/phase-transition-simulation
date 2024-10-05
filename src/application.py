from src.simulation import Simulation
from src.window import show_window

def run():
    simulation = Simulation(width=1000, height=1000, number_of_particles=100, particle_radius=4)
    show_window(resolution=(1920, 1080), simulation=simulation)
