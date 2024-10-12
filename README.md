# Spontaneous Crystallization

This project is an attempt at simulating spontaneous crystallization of particles suspended in a liquid. The particles are subject to Brownian motion.

## Quick Start
1. Clone the repo using e.g. `git clone <url>`.
2. Create a new virtual environment using `python -m venv <venv_name>`.
3. Activate the virtual environment using `source <venv_name>/scripts/activate` (e.g. on git bash for windows) or a similar command for other operating systems or terminal emulators.
4. Install the required dependencies using `pip install -r requirements.txt`.
5. Run the project using `python -u .`.

## Force Mechanism
The force due to random collisions roughly cancels out in each direction, but it doesn't completely cancel since Brownian motion exists. I take the acceleration due to the random collisions to be equal to some tunable force F divided by the mass of the particle m. The mass of the particle is proportional to its surface area (area of the circle).
