from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Create the /data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

@app.route('/')
def index():
    return render_template('index.html')

# Event listener for receiving sensor data
@socketio.on('sensor_data')
def handle_sensor_data(data):
    print(f"Received data: {data}")

    # Check for GPS data
    if 'latitude' in data and 'longitude' in data:
        with open('data/gps_data.txt', 'a') as f:
            f.write(f"Latitude: {data['latitude']}, Longitude: {data['longitude']}, Altitude: {data.get('altitude', 'N/A')}\n")

    # Check for accelerometer data
    if 'acceleration' in data:
        with open('data/accelerometer_data.txt', 'a') as f:
            f.write(f"Acceleration X: {data['acceleration']['x']}, Y: {data['acceleration']['y']}, Z: {data['acceleration']['z']}\n")

    # Check for barometer data
    if 'pressure' in data:
        with open('data/barometer_data.txt', 'a') as f:
            f.write(f"Pressure: {data['pressure']}\n")

    emit('server_response', {'message': 'Data received and logged!'})  # Acknowledge the client

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=os.getenv('PORT', 5000))
