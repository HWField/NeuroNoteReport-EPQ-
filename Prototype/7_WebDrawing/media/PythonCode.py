
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio = SocketIO(app)
@app.route("/")
def index():
    return render_template("index.html")
# Handle drawing data sent by clients
@socketio.on("draw_data")
def handle_draw_data(data):
    # Broadcast drawing data to all other clients
    emit("draw_data", data, broadcast=True, include_self=False)
 
if __name__ == '__main__':
    # Change host to '0.0.0.0' to allow external connections
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)