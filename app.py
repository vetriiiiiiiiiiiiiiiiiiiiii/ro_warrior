import streamlit as st
import time
import threading
import requests
from navigation import Navigation
from detection import SurvivorDetection
from power_management import PowerManagement
from communication import Communication
from sensors import SensorModule
from video_processing import VideoProcessing  # Import the new video processing module
from ai_model import YourModel  # Import your AI model for predictions

# Initialize modules
nav = Navigation()
detect = SurvivorDetection()
power = PowerManagement()
comm = Communication("localhost", 1883)
sensors = SensorModule()

# Initialize the AI model
model = YourModel()  # Load your trained model here
video_processor = VideoProcessing(model)  # Create an instance of VideoProcessing

# Fetch session ID from the external API
session_url = "https://roverdata2-production.up.railway.app/api/session/start"

try:
    response = requests.post(session_url)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    session_id = response.json().get("session_id", "N/A")
except requests.exceptions.RequestException as e:
    session_id = "Error fetching session ID"
    st.error(f"Failed to start session: {e}")

# Streamlit UI
st.title("Autonomous Rescue Rover Dashboard")
st.write(f"Session ID: {session_id}")

# Rover Status
st.header("Rover Status")
col1, col2 = st.columns(2)
with col1:
    st.metric("Battery Level", f"{power.battery}%")
with col2:
    st.metric("Survivors Detected", len(detect.survivors))

# Rover Position
st.header("Rover Coordinates")
st.write(f"Current Coordinates: X = {nav.x}, Y = {nav.y}")

# Sensor Readings
st.header("Sensor Readings")
sensor_data = requests.get("http://localhost:5000/api/sensor_data").json()
st.write(f"Temperature: {sensor_data['temperature']}°C")
st.write(f"Humidity: {sensor_data['humidity']}%")
st.write(f"Obstacle Detected: {'Yes' if sensor_data['obstacle'] else 'No'}")

# Survivor Detection
st.header("Survivor Detection")
if sensor_data["human_detected"]:
    if sensor_data["alive"]:
        st.success("🚑 Survivor Found: Alive")
    else:
        st.error("⚰ Survivor Found: Deceased")
else:
    st.info("No survivors detected")

# Accelerometer Data
st.header("Motion & Tilt Detection")
st.write(f"Acceleration: X = {sensor_data['accelerometer']['x']}, Y = {sensor_data['accelerometer']['y']}, Z = {sensor_data['accelerometer']['z']}")

# Tilt Warning
if sensor_data["tilt_detected"]:
    st.error("⚠️ Rover Tilted! Please check orientation.")

# Navigation Control
st.header("Navigation")
if st.button("Move Forward"):
    nav.update_position({"x": 1, "y": 0}, 1)
if st.button("Move Backward"):
    nav.update_position({"x": -1, "y": 0}, 1)
if st.button("Move Left"):
    nav.update_position({"x": 0, "y": -1}, 1)
if st.button("Move Right"):
    nav.update_position({"x": 0, "y": 1}, 1)

# Battery Management
st.header("Battery Management")
if st.button("Consume 10% Battery"):
    battery_response = requests.post("http://localhost:5000/api/update_battery", json={"consumption": 10})
    st.warning(f"Battery Level: {battery_response.json().get('battery', power.battery)}%")

if power.battery < 10:
    st.error("Battery low! Returning to base for recharge.")

# Button to view live camera
if st.button("View Live Camera"):
    st.write("Opening live camera feed...")
    # Start the OpenCV video processing in a separate thread
    video_thread = threading.Thread(target=video_processor.process_video)
    video_thread.start()