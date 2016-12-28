"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, request, send_from_directory, redirect, session
from flask import render_template, jsonify
from nocache import nocache

# DB Entities
import datetime
from google.appengine.ext import ndb

from werkzeug.security import generate_password_hash, check_password_hash

class User(ndb.Model):
	name = ndb.StringProperty()
	email = ndb.StringProperty()
	password = ndb.StringProperty()
	progress = ndb.StringProperty()  
	created = ndb.DateTimeProperty(auto_now_add=True)

# app = Flask(__name__, static_url_path="", static_folder="static")
app = Flask(__name__, template_folder = "static")
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
#app.static_url_path('public')

app.secret_key = '\xb9\x1e\xdd1L\xf6\xbbo\xeeFs\x88\xe94t\xc4\x18\x10G\xc1\xbe:\x8a\x8a'

def restrictedPath(path):
	restricted = ['Learn', 'Training', 'Videos', 'Dr', 'Coffee', 'Gaming', 'Food.', 'Special.', 'SocialMedia','Pre-food', 'TV']
	for r in restricted:
		if r in path:
			return True
	return False

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return send_from_directory('static', 'index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		userKey = ndb.Key('User', request.form['email'])

		if userKey.get():
			return jsonify(signup=False)

		newuser = User(name = request.form['name'],
		email = request.form['email'], password = generate_password_hash(request.form['password']), progress = '', id = request.form['email'])
		newuser.put()
		session['username'] = newuser.email
		session['progress'] = newuser.progress
		
		return jsonify(signup=True)

	if ('username' in session):
		return redirect('/begin')

	return send_from_directory('static', 'signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session.permanent = True
		userKey = ndb.Key('User', request.form['email'])
		user =  userKey.get()
		if not user or (not check_password_hash(user.password,request.form['password']) ):
			return jsonify(login=False)
		session['username'] = request.form['email']
		session['progress'] = user.progress
		return jsonify(login=True)

	if ('username' in session):
		return redirect('/begin')	

	return send_from_directory('static', 'login.html')


@app.route('/begin')
@nocache
def begin():
	if ('username' in session):
		if ((session['progress']) and (session['progress'] != '')):
			return send_from_directory('static', session['progress'])
		else:
			return send_from_directory('static', 'add.html')
	return redirect('/login')


@app.route('/profile', methods=['GET', 'POST'])
def profilepage():
	if ('username' in session):
		user = ndb.Key('User', session['username']).get()
		if request.method == 'POST':
			if check_password_hash(user.password,request.form['password']):
				msg = 'Password changed successfully!'
				user.password = generate_password_hash(request.form['newpassword'])
				user.put()
			else:
				msg = 'Please enter the current password correctly!'
			
			return render_template('profile.html', user = user, message = msg)

		return render_template('profile.html', user= user)
	return redirect('/login')


@app.route('/logout')
def logout():
	user = ndb.Key('User', session['username']).get()
	if user:
		user.progress = session['progress']
		user.put()
	if session['username']:
		session.pop('username', None)
	if session['progress']:
		session.pop('progress', None)
	return redirect('/')

@app.route('/<path:path>')
def sendfiles(path):
	if(not restrictedPath(path)):
		return send_from_directory('static', path)

	elif ('username' in session):
		if '.html' in path:
			return sendhtmlfiles(path)	
	return redirect('/login')

@nocache
def sendhtmlfiles(path):
	session['progress'] = path
	return send_from_directory('static', path)	


##--------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
