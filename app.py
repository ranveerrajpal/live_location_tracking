from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import os

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

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
