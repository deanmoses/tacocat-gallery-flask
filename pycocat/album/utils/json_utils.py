#
# Encode and decode Albums to/from JSON
#

# import third party libraries
import json

# import my own code
from pycocat.album.db.Album import Album
from pycocat.album.db.Photo import Photo

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

	d = json.loads(json_string)
	return Album.from_dict(d)