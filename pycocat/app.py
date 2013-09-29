import sys, os, logging
from logging import FileHandler, Formatter
from flask import Flask, jsonify, request, redirect, url_for
from flask.ext.login import LoginManager, login_required, login_user, logout_user
from werkzeug.exceptions import default_exceptions, HTTPException, Unauthorized, BadRequest
from werkzeug.utils import secure_filename
from pycocat.User import User
import pycocat.album_utils as album_utils


#
# create a JSON 200 response
#
def msg(message):
	return jsonify(message=message)

#
# create a JSON error response
#
def err(code, message):
	response = jsonify(message=message)
	response.status_code = code
	return response

def register_json_error_handlers(app):
	"""
	All error responses that you don't specifically
	manage yourself will have application/json content
	type, and will contain JSON like this:
	{ "message": "Not Found" }
	"""

	def make_json_error(ex):
		if isinstance(ex, HTTPException):
			return err(ex.code, str(ex.name))
		elif isinstance(ex, NotImplementedError):
			return err(501, 'Not yet implemented')
		elif app.debug:
			return err(500, str(ex))
		else:
			return err(500, 'Server error')

	for code in default_exceptions.iterkeys():
		app.error_handler_spec[None][code] = make_json_error

# The root of my Flask app.
# The 'app' function is what's imported by the cgi
# script, passenger_wsgi.py
app = Flask(__name__)
register_json_error_handlers(app)

#
# Set up photo uploads
#
app.config['UPLOAD_FOLDER'] = os.getcwd() # where to save photos
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # restrict uploads to 16MB
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#
# Set up logging
#
if not app.debug:
	file_handler = FileHandler('app.log')
	file_handler.setLevel(logging.INFO)
	file_handler.setFormatter(Formatter(
		'%(asctime)s: %(message)s '
		'[in %(pathname)s:%(lineno)d]'
	))
	app.logger.addHandler(file_handler)

#
# handle a set password request
#
@app.route("/register", methods=['GET', 'POST'])
def register_user():
	username = request.args.get('username')
	password = request.args.get('password')
	if not username: raise BadRequest(description='Missing username')
	if not password: raise BadRequest(description='Missing password')

	try:
		User.create(username, password)
	except ValueError:
		raise BadRequest(description='Invalid user info')

	return msg('Created user')


#
# handle login request
#
@app.route('/login', methods=['POST'])
def login():
	username = None
	password = None

	try:
		username = request.form['username']
	except KeyError:
		raise BadRequest(description='Missing username')

	try:
		password = request.form['password']
	except KeyError:
		raise BadRequest(description='Missing password')

	# for now fake a user
	user = User.get(username, password)

	if not user:
		raise Unauthorized(description='Invalid username/password combination')

	# If we're on tacocat (as opposed to a local
	# dev box), set the cookies so that they can
	# cross domains:  meaning, a page served from
	# tacocat.com can send it back to flask.tacocat.com
	if 'tacocat.com' in request.environ['SERVER_NAME']:
		app.config['REMEMBER_COOKIE_DOMAIN'] = '.tacocat.com'

	# Sets up the session cookies in the response
	# remember=True sets a long term cookie
	login_user(user, remember=True)

	# Give client their authentication status
	return jsonify(isAuthenticated=True, isSiteAdmin=True)

#
# handle logout request
#
@app.route('/logout', methods=['POST'])
def logout():
	logout_user()
	return jsonify(isAuthenticated=False, isSiteAdmin=False)

#
# client is wanting to know whether it's authenticated or not
#
@app.route('/auth_status', methods=['GET'])
@login_required
def auth_status():
	# if they aren't authenticated, they get a 401 and don't reach here
	return jsonify(isAuthenticated=True, isSiteAdmin=True)

#
# photo upload
#
@app.route('/upload', methods=['POST'])
@login_required
def upload():
	app.logger.debug('doUpload()')
	file = request.files['file']

	# make sure a file was sent
	if not file:
		raise BadRequest(description='No file')

	# make sure it's a jpg or png
	if not allowed_file(file.filename):
		raise BadRequest(description='filename not allowed: [%s]' % file.filename)

	# ensure filename won't cause security issues
	filename = secure_filename(file.filename)

	# save file
	# TODO: get path to album
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

	# tell client it's all cool
	return msg('Uploaded: ' + filename)

#
# Album web service:
# POST:  create album
# PATCH: update just some properties of the album
# PUT: replace the entire album
# GET: not supported, we retrieve albums via the filesystem .json
#
@app.route('/album/<path:album_path>', methods=['POST'])
@login_required
def album(album_path):
	app.logger.debug('/album/' + album_path)

	title = request.args.get('title')
	summary = request.args.get('summary')

	# create album on disk
	# album will validate path, title, summary
	# and whether it already exists
	album_utils.create_album(album_path, title, summary)



#
# test route for whenever I need to try out something
#
@app.route('/test', methods=['GET', 'POST', 'PUT', 'PATCH'])
@login_required
def test():
	app.logger.debug('/test')

	#return "path: %s" %  path

	#if request.method != 'PUT':
	#	return jsonify(error = '%s requests are not supported' % request.method)

	if request.data:
		parsedJson = request.get_json(force=True)

		if len(parsedJson) > 0:
			app.logger.error('parsed JSON: [%s]', str(parsedJson))

			#import admin.photo as photo
			#photo.save(path, parsedJson)

			return jsonify(success=True)

	return "END"

#
# error handling test
#
@app.route("/test/error", methods=['GET', 'POST', 'PUT', 'PATCH'])
def fake_err():
	app.logger.debug('fake_err()')
	raise Exception('This is a fake exception')


#
# Set up authentication system
#

login_manager = LoginManager()

#
# Register callback to look up the user object.
# This is only called if the user is already
# authenticated, and we just need to retrieve
# the full User object back for the request.
#
@login_manager.user_loader
def load_user(username):
	if username:
		return User(username)
	else:
		return None

# needed by authentication system
with open(os.path.join(os.getcwd(), 'secret.txt'), 'r') as f:
	app.secret_key = f.read()

login_manager.init_app(app)

# If this script is run directly (e.g. from the command line) 
# instead of being imported into some other script, run it.
# This allows the script to be run in debug mode from the command line.
if __name__ == "__main__":
	# debug=True: server will reload itself on code changes
	# Also provides you with a helpful debugger if things go wrong
	app.run(debug=False)
