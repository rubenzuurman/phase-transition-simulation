class Camera:
    
    def __init__(self):
        self.position = [0, 0]
        self.zoom = 1
    
    def move_to(self, position):
        self.position = position
    
    def move_by(self, offset):
        self.position[0] += offset[0]
        self.position[1] += offset[1]
    
    def get_position(self):
        return self.position
    
    def get_zoom(self):
        return self.zoom
