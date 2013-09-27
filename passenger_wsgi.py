# The job of this script is to import and create a Python variable named 'application'
# that is available to the Passenger WSGI container

import sys, os

# Switch to the virtualenv at ./flask_env/bin/pythong if we're not already there
INTERP = os.path.join(os.environ['HOME'], 'flask_env', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# append current dir to module path
sys.path.append(os.getcwd())

# append the Album dir to module path
albumModuleDir = os.path.join(os.environ['HOME'], 'scrape', 'mylib')
sys.path.append(albumModuleDir)

# Import the 'app' function defined in pycocat/app.py
# This is what the Passenger FastCGI system looks for and executes each request
from pycocat.app import app as application

# Uncomment next two lines to enable debugging
#if DEBUG:
#	application.debug = True
from werkzeug.debug import DebuggedApplication
application.wsgi_app= DebuggedApplication(application.wsgi_app, evalex=True)
