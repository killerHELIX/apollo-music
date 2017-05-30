import os
import sys
from pymongo import MongoClient
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request
app = Flask(__name__)

# prevents UnicodeDecodeError
reload(sys)
sys.setdefaultencoding('utf8')

socketio = SocketIO(app)
client = MongoClient('localhost', 27017)

@socketio.on('connect')
def makeConnection():
    print('Connected.')
    
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
