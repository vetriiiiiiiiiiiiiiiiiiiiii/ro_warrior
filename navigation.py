class Navigation:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update_position(self, movement, step):
        """Update position dynamically based on movement"""
        self.x += movement["x"] * step
        self.y += movement["y"] * step

    def get_position(self):
        return {"x": self.x, "y": self.y}