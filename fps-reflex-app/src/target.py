import math

class Target:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def is_clicked(self, mouse_x, mouse_y):
        distance = math.sqrt((mouse_x - self.x)**2 + (mouse_y - self.y)**2)
        return distance <= self.size