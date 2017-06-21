import os
import sys
from pymongo import MongoClient
import pprint
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, session, redirect
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')
bcrypt = Bcrypt(app)

# prevents UnicodeDecodeError
reload(sys)
sys.setdefaultencoding('utf8')


socketio = SocketIO(app)
client = MongoClient('localhost', 27017)
db = client['apollo']
allTracks = db['tracks']
allUsers = db['users']

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
	
	# initialize session variables
	if 'user' not in session:
		session['user'] = None
		
	print(request.method)
	return render_template('index.html')
    
@app.route('/listener', methods=['GET', 'POST'])
def renderUser():
    print(request.method)
    return render_template('listener.html')
    
@app.route('/owner', methods=['GET', 'POST'])
def renderSuper():
    print(request.method)
    return render_template('owner.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
	print("Entered login on server.py")
	
	# if the user clicks submit, validate input
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		print("User entered some stuff, check it: " + username + ", " + password)
		
		try:
			print("Printing all users...")
			for user in allUsers.find():
				pprint.pprint(user)
			print("Searching for " + username + "...")
			result = allUsers.find_one({"username":username})
			if result is None:
				print(username + " does not exist!")
				return render_template('login.html', success=False, redirected=False)

			elif bcrypt.check_password_hash(result['password'], password):
				print("Through the power of cryptography, you're clear to login. (validation successful)")
				session['user'] = username
				
				return render_template("index.html")
			else:
				print("document: " + result['username'] + ", " + result['password'])
				print("Filthy scum, this account is not yours to plunder. (validation failed)")
				return render_template('login.html', success=False, redirected=False)
			
		except Exception as e:
			print("Some shit went wrong. Form inputs may be empty.")
			print(e)
			# emit something
		
	return render_template('login.html', success=True)
	
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	print("Entered logout on server.py")
	print("Setting session variables to default...")
	session['user'] = None
	print("Done.")
	
	return render_template("index.html")
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	print("Entered register on server.py")
	
	# if the user clicks register, validate input
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		info = {'username':username, 'password':password}
		existence = allUsers.find({'username':username})
		if existence is None:
			print("Username not taken.  Insert that bitch.")
			success = allUsers.insertOne(info)
			if success.acknowledged:
				print("Inserted successfully.")
				return render_template("login.html", redirected=True)
			else:
				print("Insertion failed.")
				return render_template("register.html", success="InsertionFailed")
		else:
			print("Username already taken.  Don't insert shit.")
			return render_template("register.html", success="UsernameTaken")
	
	return render_template("register.html")
	
# start the server
if __name__ == '__main__':
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
