class SurvivorDetection:
    def __init__(self):
        self.survivors = []

    def detect_survivor(self, location):
        """Detects a survivor and adds their location"""
        self.survivors.append(location)