import os
import sys
import random
from pymongo import MongoClient
import pprint
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, session, redirect
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).encode('hex')
bcrypt = Bcrypt(app)

# prevents UnicodeDecodeError
reload(sys)
sys.setdefaultencoding('utf8')


socketio = SocketIO(app)
client = MongoClient('localhost', 27017)
db = client['apollo']
tracks = db['tracks']
users = db['users']

@socketio.on('connect')
def makeConnection():
    print('Connected.')
    
    print("Printing all tracks...")
    # for track in tracks.find():
    #     pprint.pprint(track)
    print("Just kidding.  There's a lot.")
  
	
@socketio.on('findTrack')
def findTrack(track):
	print("Entered findTrack in server.py with param track['title']" + track['title'])
	print("Searching for tracks with title " + track['title'])
	for track in tracks.find({'title':track['title']}):
		print(str(track['_id']) + ', ' + track['title'])
		emit('foundTrack', track)
	
@socketio.on('debugPopulateDB')
def debug():
	print("Entered debugPopulateDB in server.py")
	inserted_tracks = []
	custom_index = ['A', 'B', 'C']
	subtracks = ['a', 'b', 'c', 'd', 'e', 'f']
	urls = ['10sec.m4a', 'LetGoArkPatrol.webm', 'Prismo.webm', 'RickRoll.webm']
	genres = ['Light combat', 'Heavy combat', 'Light town', 'Heavy town', 'Monster Condom', 'Magnum Dong']
	count = 1;
	
	# iterate horizontally (left->right)
	for index in custom_index:
		# iterate vertically (low->high)
		for i in range(1,4):
			# add the track to payload
			tmpTrack = {
				'_id': count,
				'title': index + str(i) + ' Full',
				'genre': random.choice(genres),
				'url': 'static/media/' + random.choice(urls),
				'subtracks': []
			}
			count = count + 1
			
			# slap on a subtrack for each track
			for sub in subtracks:
				print(index + str(i) + sub)
				tmpSub = {
					"_id": count,
					'title': index + str(i) + sub,
					'genre': random.choice(genres),
					'url': 'static/media/' + random.choice(urls),
					'subtracks': []
				}
				
				# append to subtrack key:value pair
				tmpTrack['subtracks'].append(tmpSub)
				count = count + 1
			
			# fire payload
			inserted_tracks.append(tmpTrack)
	
	print("Would have inserted these tracks: ")
	for track in inserted_tracks:
		print(track['title'] + ', ' + str(track['_id']))
		if track['subtracks']:
			for sub in track['subtracks']:
				print(sub['title'] + ', ' + str(sub['_id']))
				
	# drop that monster condom for your magnum dong
	try:
		for track in inserted_tracks:
			tracks.insert_one(track)
			if track['subtracks']:
				for sub in track['subtracks']:
					tracks.insert_one(sub)
					
	except Exception as e:
		print("This monster condom wasn't the right one... (insertion of magnum dong failed),")
		print(e)
		
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
			for user in users.find():
				pprint.pprint(user)
			print("Searching for " + username + "...")
			result = users.find_one({"username":username})
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
			print("Some shit went wrong. See error below.")
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
		
		info = {
			'username':username, 
			'password':bcrypt.generate_password_hash(password).decode('utf-8')
		}
		
		existence = users.find({'username':username})
		print("existence: ")
		print(existence.count())
		if existence.count() is 0:
			print("Username not taken.  Insert that bitch.")
			success = users.insert_one(info)
			if success.acknowledged:
				print("Inserted successfully.")
				return render_template("login.html", fromRegister=True, success=True)
			else:
				print("Insertion failed.")
				return render_template("register.html", status="InsertionFailed")
		else:
			print("Username already taken.  Don't insert shit.")
			return render_template("register.html", status="UsernameTaken")
	
	return render_template("register.html")
	
# start the server
if __name__ == '__main__':
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
