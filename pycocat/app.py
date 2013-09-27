import sys, os, logging
from flask import Flask
from flask import request
from flask import jsonify

from flask.ext.login import login_required

from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException



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


@app.route("/<path:path>", methods=['GET', 'POST', 'PUT', 'PATCH'])
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



# Set up authentication system
from flask.ext.login import LoginManager

login_manager = LoginManager()


@login_manager.user_loader
def load_user(userid):
	return None

# needed by authentication system
# just a random string
app.secret_key = 'y FN- 0823hf2j fc 028  -)* n3!&aMR'

login_manager.init_app(app)
'''
try:
	login_manager.init_app(application)
except Exception as e:
	logFile = os.path.join(os.environ['HOME'], 'flask_env', 'a.log')
	with open(logFile, 'a') as log:
		log.write("error: %s" % (e))
	pass
'''
# If this script is run directly (e.g. from the command line) 
# instead of being imported into some other script, run it.
# This allows the script to be run in debug mode from the command line.
if __name__ == "__main__":
	# debug=True: server will reload itself on code changes
	# Also provides you with a helpful debugger if things go wrong
	app.run(debug=True)
