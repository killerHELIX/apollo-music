import os
import sys
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request
app = Flask(__name__)

# prevents UnicodeDecodeError
reload(sys)
sys.setdefaultencoding('utf8')

socketio = SocketIO(app)

@socketio.on('connect')
def makeConnection():
    print('Connected.')
    
@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    print(request.method)
    return render_template('index.html')
    
# start the server
if __name__ == '__main__':
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
