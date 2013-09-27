import sys, os, logging
from logging import FileHandler, Formatter
from flask import Flask, jsonify, request, redirect, url_for
from flask.ext.login import LoginManager, login_required, login_user, logout_user
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.utils import secure_filename
from pycocat.User import User


def register_json_error_handlers(app):
	"""
	All error responses that you don't specifically
	manage yourself will have application/json content
	type, and will contain JSON like this:
	{ "message": "Not Found" }
	"""

	def make_json_error(ex):
		if isinstance(ex, HTTPException):
			response = jsonify(message=str(ex.name))
			response.status_code = (ex.code)
		else:
			if app.debug:
				response = jsonify(message=str(ex))
			else:
				response = jsonify(message='Server error')
			response.status_code = 500
		return response

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
# create a JSON 200 response
#
def msg(message):
	return jsonify(message=message)

#
# create a JSON response
#
def err(status_code, message):
	response = jsonify(message=message)
	response.status_code = status_code
	return response

#
# handle a set password request
#
@app.route("/register", methods=['GET', 'POST'])
def register_user():
	username = request.args.get('username')
	password = request.args.get('password')
	if not username: return err(400, 'Missing username')
	if not password: return err(400, 'Missing password')

	try:
		User.create(username, password)
	except ValueError:
		response = jsonify(message='Invalid user info')
		response.status_code = 400
		return response

	return jsonify(message='Created user')


#
# handle login request
#
@app.route("/login", methods=['GET', 'POST'])
def login():
	username = request.args.get('username')
	password = request.args.get('password')

	if not username: return err(400, 'Missing username')
	if not password: return err(400, 'Missing password')

	# for now fake a user
	user = User.get(username, password)

	if not user:
		response = jsonify(message='Invalid username/password combination')
		response.status_code = 401
		return response


	# If we're on tacocat (as opposed to a local
	# dev box), set the cookies so that they can
	# cross domains:  meaning, a page served from
	# tacocat.com can send it back to flask.tacocat.com
	if 'tacocat.com' in request.environ['SERVER_NAME']:
		app.config['REMEMBER_COOKIE_DOMAIN'] = '.tacocat.com'

	# Sets up the session cookies in the response
	# remember=True sets a long term cookie
	login_user(user, remember=True)

	# Let client know everything's cool
	return jsonify(message='Successful login')

#
# handle logout request
#
@app.route("/logout", methods=['GET', 'POST'])
def logout():
	logout_user()
	return jsonify(message="Successful logout")

#
# photo upload
#
@app.route("/upload", methods=['POST'])
@login_required
def upload():
	app.logger.debug('doUpload()')
	file = request.files['file']

	# make sure file was sent
	if not file:
		return jsonify(400, 'No file')

	# make sure it's a jpg or png
	if not allowed_file(file.filename):
		return jsonify(400, 'filename not allowed: [%s]' % file.filename)

	# ensure filename won't cause security issues
	filename = secure_filename(file.filename)

	# save file
	# TODO: get path to album
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

	# tell client it's all cool
	return jsonify(message='Uploaded: ' + filename)

#
# authentication test
#
@app.route("/", methods=['GET', 'POST', 'PUT', 'PATCH'])
@login_required
def index():
	app.logger.debug('index()')

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
@app.route("/err", methods=['GET', 'POST', 'PUT', 'PATCH'])
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
# just a random string
app.secret_key = 'y FN- 0823hf2j fc 028  -)* n3!&aMR'

login_manager.init_app(app)

# If this script is run directly (e.g. from the command line) 
# instead of being imported into some other script, run it.
# This allows the script to be run in debug mode from the command line.
if __name__ == "__main__":
	# debug=True: server will reload itself on code changes
	# Also provides you with a helpful debugger if things go wrong
	app.run(debug=True)
