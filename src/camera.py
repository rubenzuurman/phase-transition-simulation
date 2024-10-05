class Camera:
    
    def __init__(self):
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.zoom = 1
        self.zoom_target = 1
    
    def update(self, delta):
        # Move camera.
        self.position[0] += self.velocity[0] * delta / self.get_zoom()
        self.position[1] += self.velocity[1] * delta / self.get_zoom()
        
        # Manage zoom.
        zoom_speed = 10 # Tunable: higher means faster conversion, but higher chance of unstability at (very) low framerates.
        zoom_error = self.zoom_target - self.zoom
        self.zoom += zoom_speed * zoom_error * delta
    
    def move_to(self, position):
        self.position = position
    
    def move_by(self, offset):
        self.position[0] += offset[0]
        self.position[1] += offset[1]
    
    def get_position(self):
        return self.position
    
    def get_velocity(self):
        return (self.velocity[0] / self.get_zoom(), self.velocity[1] / self.get_zoom())
    
    def set_velocity(self, velocity):
        self.velocity = velocity
    
    def get_zoom(self):
        return self.zoom
    
    def get_zoom_target(self):
        return self.zoom_target
    
    def set_zoom_target(self, zoom_target):
        self.zoom_target = zoom_target
