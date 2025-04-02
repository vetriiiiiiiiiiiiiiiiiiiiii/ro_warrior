import random

class SensorModule:
    def __init__(self):
        self.temperature = 25  # Default temperature in Celsius
        self.humidity = 50  # Default humidity in percentage
        self.obstacle = False
        self.human_detected = False
        self.alive = False
        self.accelerometer = {"x": 0.0, "y": 0.0, "z": 1.0}  # Default acceleration
        self.tilt_detected = False

    def get_readings(self):
        """Simulate real-time sensor data"""
        self.temperature = random.uniform(20, 30)  # Simulated temp changes
        self.humidity = random.uniform(40, 60)  # Simulated humidity changes
        self.obstacle = random.choice([True, False])  # Random obstacle detection
        self.human_detected = random.choice([True, False])  # Simulated human detection
        self.alive = self.check_vitals() if self.human_detected else False  # Check if alive
        self.accelerometer = self.get_accelerometer_data()  # Get acceleration values
        self.tilt_detected = self.detect_tilt()  # Check for tilt

        return {
            "temperature": round(self.temperature, 2),
            "humidity": round(self.humidity, 2),
            "obstacle": self.obstacle,
            "human_detected": self.human_detected,
            "alive": self.alive,
            "accelerometer": self.accelerometer,
            "tilt_detected": self.tilt_detected
        }

    def detect_obstacle(self):
        """Returns True if an obstacle is detected"""
        return self.obstacle

    def check_vitals(self):
        """Simulates heartbeat and breathing detection to determine if a human is alive"""
        heartbeat = random.randint(50, 120)  # Simulated heartbeat (normal: 60-100)
        breathing_rate = random.randint(10, 20)  # Simulated breathing rate (normal: 12-16)
        return heartbeat > 50 and breathing_rate > 10  # Basic threshold for being alive

    def get_accelerometer_data(self):
        """Simulates accelerometer readings for motion detection"""
        return {
            "x": round(random.uniform(-1, 1), 2),  # Simulated x-axis movement
            "y": round(random.uniform(-1, 1), 2),  # Simulated y-axis movement
            "z": round(random.uniform(0.5, 1.5), 2)  # Simulated z-axis (gravity effect)
        }

    def detect_tilt(self):
        """Detect if rover is tilted (based on z-axis acceleration)"""
        return self.accelerometer["z"] < 0.8  # If z < 0.8, assume the rover is tilted