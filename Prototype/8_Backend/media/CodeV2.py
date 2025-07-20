from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secret key of your choice
socketio = SocketIO(app, cors_allowed_origins="*")
# Create an SQLite database
engine = create_engine('sqlite:///notes.db')
Base = declarative_base()
dbSession = sessionmaker(bind=engine)
dbsession = dbSession()

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
 
class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


Base.metadata.create_all(engine)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    elements = []
 
    
    # Retrieve all tags and add them as nodes
    tags = dbsession.query(Tag).all()
    for tag in tags:
        node = {
            'data': {
                'id': f"tag_{tag.id}",
                'label': tag.name,
                'depth': tag.get_depth()
            },
            'classes': 'tag'
        }
        elements.append(node)
  
    notes = dbsession.query(Note).all()
    for note in notes:
        node = {
            'data': {
                'id': f"note_{note.id}",
                'label': note.name
            },
            'classes': 'note'
        }

    return jsonify(elements=elements)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)
