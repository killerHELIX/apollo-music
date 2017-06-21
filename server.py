import os
import sys
from pymongo import MongoClient
import pprint
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, session
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)

# prevents UnicodeDecodeError
reload(sys)
sys.setdefaultencoding('utf8')

socketio = SocketIO(app)
client = MongoClient('localhost', 27017)
db = client['apollo']
allTracks = db['tracks']
allUsers = db['users']


# SESSION VARIABLES
session['loggedIn'] = False
session['user'] = None


@socketio.on('connect')
def makeConnection():
    print('Connected.')
    
    # print("Printing all tracks...")
    # for track in allTracks.find():
    #     pprint.pprint(track)
        
@socketio.on('findTrack')
def findTrack(track):
	print("Entered findTrack in server.py with param " + track)
	
@socketio.on('validateLogin')
def validateLogin(username, password):
	try:
		print("Entered validateLogin on server.py with params " + username + ", " + password)
		# pw = bcrypt.generate_password_hash(password)
		# print(password + " hashed into " + pw)
		print("Printing all users...")
		for user in allUsers.find():
			pprint.pprint(user)
		print("Searching for " + username + "...")
		result = allUsers.find_one({"username":username})
		if result is None:
			print(username + " does not exist!")
			# emit something
		elif bcrypt.check_password_hash(result['password'], password):
			print("Through the power of cryptography, you're clear to login. (validation successful)")
			# emit something
		else:
			print("document: " + result['username'] + ", " + result['password'])
			print("Filthy scum, this account is not yours for plunder. (validation failed)")
			# emit something
			
	except Exception as e:
		print("Some shit went wrong. Form inputs may be empty.")
		print(e)
		# emit something
		
@socketio.on('registerNew')
def registerNew(username, password):
	print("Entered registerNew on server.py with params " + username + ", " + password)
	
	# generate JSON object to insert
	userInfo = {'username': username, 'password': bcrypt.generate_password_hash(password)}
	success = allUsers.insert_one(userInfo)
	if success.acknowledged:
		print("Insertion successful!")
		# emit something
	else:
		print("Insertion failed.")
		# emit something
    
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
    
@app.route('/login.html', methods=['GET', 'POST'])
def login():
	print("Entered /login/ on server.py")
    
# start the server
if __name__ == '__main__':
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
