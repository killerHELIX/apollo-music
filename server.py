import os
import sys
from pymongo import MongoClient
import pprint
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request
app = Flask(__name__)

# prevents UnicodeDecodeError
reload(sys)
sys.setdefaultencoding('utf8')

socketio = SocketIO(app)
client = MongoClient('localhost', 27017)
db = client['apollo']
collection = db['tracks']


@socketio.on('connect')
def makeConnection():
    print('Connected.')
    
    print("Printing database entries...")
    for entry in collection.find():
        pprint.pprint(entry)
        
@socketio.on('findTrack')
def findTrack(track):
	print("Entered findTrack in server.py with param " + track)
	
@socketio.on('validateLogin')
def validateLogin(username, password):
	print("Entered validateLogin on server.py with params " + username + ", " + password)
    
@app.route('/', methods=['GET', 'POST'])
def renderIndex():
    print(request.method)
    return render_template('index.html')
    
@app.route('/listener.html', methods=['GET', 'POST'])
def renderUser():
    print(request.method)
    return render_template('listener.html')
    
@app.route('/owner.html', methods=['GET', 'POST'])
def renderSuper():
    print(request.method)
    return render_template('owner.html')
    
# start the server
if __name__ == '__main__':
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
