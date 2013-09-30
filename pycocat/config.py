"""
Configuration of both the scrape script and the album store - exposes paths and such
"""

WEB_DIR = None # root dir of tacocat webserver on disk
ALBUM_DATA_DIR = None # root dir of album YAML files on disk
ALBUM_WEB_DIR = None # root dir of album JSON files on disk

debug = True

if debug:
	WEB_DIR = '/Users/dmoses/Sites/oldpix'
	ALBUM_DATA_DIR = WEB_DIR
	ALBUM_WEB_DIR = ALBUM_DATA_DIR

else:
	WEB_DIR = '/home/deanmoses/themosii.com'
	ALBUM_DATA_DIR = WEB_DIR + '/oldpix'
	ALBUM_WEB_DIR = ALBUM_DATA_DIR