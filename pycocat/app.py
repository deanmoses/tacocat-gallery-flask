import sys, os, logging
from flask import Flask, jsonify, request, redirect, url_for
from flask.ext.login import LoginManager, login_required
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.utils import secure_filename
from pycocat import User

__all__ = ['make_json_app']

def make_json_app(import_name, **kwargs):
	"""
	Creates a JSON-oriented Flask app.

	All error responses that you don't specifically
	manage yourself will have application/json content
	type, and will contain JSON like this (just an example):

	{ "message": "405: Method Not Allowed" }
	"""

	def make_json_error(ex):
		response = jsonify(message=str(ex))
		response.status_code = (ex.code
								if isinstance(ex, HTTPException)
								else 500)
		return response

	app = Flask(import_name, **kwargs)
	doJsonErrors = False
	if doJsonErrors:
		for code in default_exceptions.iterkeys():
			app.error_handler_spec[None][code] = make_json_error

	return app

#
# The root of my Flask app.
# The 'app' function is what's imported by the cgi
# script, passenger_wsgi.py
#
#app = Flask(__name__)
app = make_json_app(__name__)

#
# Set up photo uploads
#

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # restrict uploads to 16MB

#
# Set up logging
#
if not app.debug:
	import logging
	from logging import FileHandler

	file_handler = FileHandler('app.log')
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)


@app.errorhandler(404)
def not_found(error=None):
	resp = jsonify(status=404, message='Not Found: ' + request.url)
	resp.status_code = 404
	return resp

#
# photo upload
#
@app.route("/upload", methods=['POST'])
def doUpload():
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
# authentication
#
@app.route("/login", methods=['GET', 'POST', 'PUT', 'PATCH'])
@login_required
def doMain(path):
		app.logger.debug('doMain()')

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
# Set up authentication system
#

login_manager = LoginManager()

#
# register callback to look up the user object
#
@login_manager.user_loader
def load_user(username):
	return User.get(username)

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
