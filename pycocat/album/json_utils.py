#
# Encode and decode Albums to/from JSON
#

# import third party libraries
import json

# import my own code
from Album import Album
from Photo import Photo

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)


class AlbumEncoder(json.JSONEncoder):
	"""
	handles encoding an Album and its child Photo objects as JSON
	"""
	def default(self, o):
		return o.__dict__


def album_decoder (dict):
	"""
	handles decoding JSON into objects
	"""
	if 'children' in dict or 'photos' in dict or 'childAlbumThumbs' in dict:
		return Album(dict)
	if 'fullSizeImage' in dict and not 'creationTimestamp' in dict:
		return Photo(dict)
	else:
		return dict


def to_string(album):
	"""
	Return specified Album as a JSON string

	Parameters
	----------
	album : Album
	   album to return as JSON string

	Return
	----------
	JSON string representing album
	"""

	jsonString = json.dumps(album.to_dict(), sort_keys=True,
	               indent=4, separators=(',', ': '))

	return jsonString


def from_string(json_string):
	"""
	Return specified JSON string as an Album object

	Parameters
	----------
	jsonString : string
	   JSON string representing an Album

	Return
	----------
	Album object
	"""

	#return json.loads(json_string, object_hook=album_decoder)
	d = json.loads(json_string)
	return Album.from_dict(d)