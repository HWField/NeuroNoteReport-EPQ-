from flask import Flask, render_template
from flask_socketio import SocketIO, emit
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)
shared_text = {'content': ''}
@app.route('/')
def index():
    return render_template('index.html')
@socketio.on('text_update')
def handle_text_update(data):
    # Update shared content based on the received changes
    shared_text['content'] = data['content']
    emit('text_update', data, broadcast=True, include_self=False)
# Send the current content to a new user on connection
@socketio.on('connect')
def handle_connect():
    emit('text_update', {'content': shared_text['content'], 'position': 0, 'length': len(shared_text['content'])})
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)