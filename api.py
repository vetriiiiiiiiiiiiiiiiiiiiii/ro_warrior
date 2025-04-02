from flask import Flask, jsonify, request
from navigation import Navigation
from detection import SurvivorDetection
from power_management import PowerManagement
from sensors import SensorModule

app = Flask(__name__)

# Initialize modules
nav = Navigation()
detect = SurvivorDetection()
power = PowerManagement()
sensors = SensorModule()

@app.route('/api/start_session', methods=['POST'])
def start_session():
    return jsonify({"session_id": "12345"})

@app.route('/api/rover_status', methods=['GET'])
def get_rover_status():
    status = {
        "position": nav.get_position(),
        "battery": power.battery,
        "survivors": detect.survivors,
        "sensors": sensors.get_readings()
    }
    return jsonify(status)

@app.route('/api/update_battery', methods=['POST'])
def update_battery():
    data = request.json
    power.update_battery(data.get('consumption', 1))
    return jsonify({"battery": power.battery})

@app.route('/api/update_position', methods=['POST'])
def update_position():
    """Update rover position"""
    data = request.json
    if sensors.detect_obstacle():
        return jsonify({"error": "Obstacle detected! Cannot move."}), 400
    nav.x = data.get("x", nav.x)
    nav.y = data.get("y", nav.y)
    return jsonify({"message": "Position updated", "position": nav.get_position()})

@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    """Fetch latest sensor data including accelerometer and tilt"""
    return jsonify(sensors.get_readings())

if __name__ == '__main__':
    app.run(debug=True, port=5000)