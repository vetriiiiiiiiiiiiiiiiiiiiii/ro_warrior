class PowerManagement:
    def __init__(self):
        self.battery = 100

    def update_battery(self, consumption):
        """Reduce battery level based on consumption"""
        self.battery = max(0, self.battery - consumption)