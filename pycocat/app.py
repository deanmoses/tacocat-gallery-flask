import sys, os, logging
from flask import Flask
from flask import request
from flask import jsonify

from album.NotFoundException import NotFoundException

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
	
@app.route("/<path:path>", methods=['GET', 'POST', 'PUT'])
def doMain(path):
	try:
		app.logger.error('doMain()')
		
		#return "path: %s" %  path
		
		#if request.method != 'PUT':
		#	return jsonify(error = '%s requests are not supported' % request.method)
		

		try:
			parsedJson = request.get_json(force=True)
			if len(parsedJson) > 0:
				app.logger.error('parsed JSON: [%s]', str(parsedJson))

				import admin.photo as photo
				photo.save(path, parsedJson)
				
				return jsonify(success=True)
		except NotFoundException, inst:
			return str(inst), 404
		except TypeError, inst:
			msg = 'TypeError: %s' % str(inst)
			app.logger.error(msg)
			resp = jsonify(error=msg)
			resp.status_code = 500
			return resp

		return "END"
		
	except AttributeError, inst:
		msg = 'AttributeError: %s' % str(inst)
		app.logger.error(msg)
		resp = jsonify(error=msg)
		resp.status_code = 500
		return resp
		
	except SyntaxError, inst:
		msg = 'SyntaxError: %s' % str(inst)
		app.logger.error(msg)
		resp = jsonify(error=msg)
		resp.status_code = 500
		return resp
	except Exception, inst:
		msg = 'Exception: %s' % str(inst)
		app.logger.error(msg)
		resp = jsonify(error=msg)
		resp.status_code = 500
		return resp


# If this script is run directly (e.g. from the command line) 
# instead of being imported into some other script, run it.
# This allows the script to be run in debug mode from the command line.
if __name__ == "__main__":
    app.run()
