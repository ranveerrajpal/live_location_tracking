from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import os
import random
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

# Route to serve the index.html directly
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

# WebSocket event handler for receiving sensor data
@socketio.on('sensor_data')
def handle_sensor_data(data):
    print("Received sensor data:", data)
    # Send back a response to the frontend
    socketio.emit('server_response', {'message': 'Data received successfully'})

def send_sensor_data():
    """Simulate sending sensor data every second."""
    while True:
        # Simulated sensor data with random x and y coordinates
        data = {
            'x': random.randint(0, 490),  # Random X coordinate within bounds
            'y': random.randint(0, 490)   # Random Y coordinate within bounds
        }
        socketio.emit('sensor_data', data)  # Emit data to all connected clients
        time.sleep(1)  # Send data every second

# Start the sensor data sending in a separate thread
threading.Thread(target=send_sensor_data, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
