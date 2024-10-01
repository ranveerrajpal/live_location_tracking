from flask import Flask, render_template
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

# Route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket event handler for receiving sensor data
@socketio.on('sensor_data')
def handle_sensor_data(data):
    print("Received sensor data:", data)
    # Send back a response to the frontend
    socketio.emit('server_response', {'message': 'Data received successfully'})

# Remove the run block
if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
