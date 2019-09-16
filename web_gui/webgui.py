import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mindflayer"
app.config["SECRET_KEY"] = 'mysecret'
mongo = PyMongo(app)
bootstrap = Bootstrap(app)
socketio = SocketIO(app, logger=True, engineio_logger=True)

session_collection = mongo.db.Sessions
event_collection = mongo.db.Event
recon_collection = mongo.db.Reconnaissance

def session_emit():
    resume_token = None
    pipeline = [{'$match': {'operationType': 'insert'}}]
    with mongo.db.Sessions.watch(pipeline) as stream:
        for change in stream:
            socketio.emit('new session', change['fullDocument'])
            resume_token = stream.resume_token

def event_emit():
    resume_token = None
    pipeline = [{'$match': {'operationType': 'insert'}}]
    with mongo.db.Event.watch(pipeline) as stream:
        for change in stream:
            # print(change['fullDocument']['calledEvent'])
            socketio.emit('new event', change['fullDocument']['calledEvent'])
            resume_token = stream.resume_token

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)

@app.route("/")
def home_page():
    session = session_collection.find({})
    event = event_collection.find({})
    recon = recon_collection.find({})
    return render_template("index.html", session=session, event=event, recon=recon)

eventlet.spawn(session_emit)
eventlet.spawn(event_emit)

if __name__ == '__main__':
    socketio.run(app, port=7000, debug=True)