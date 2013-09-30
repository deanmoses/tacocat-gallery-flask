import os
import json_utils, file_utils
import pycocat.config as config
from Album import Album
from pycocat.album.album_exceptions import AlbumException, FoundException, NotFoundException
import album_utils

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

def save(album_path, album, create=False):
	"""
	Parameters
	----------
	create: boolean
		True: save new album. Fails if album already exists.
		False: update existing album. Fails if album doesn't already exist.
	"""

	# raises exception if album has missing or invalid fields
	album.validate()

	# convert album object into JSON string
	album_string = json_utils.to_string(album)

	# get full path to album's JSON file on disk
	file_path = __file_path(album_path)

	# write to disk
	if create:
		try:
			file_utils.create_file(file_path, album_string)
		except AssertionError:
			raise FoundException("Album [%s] already exists" % album_path)
	else:
		try:
			file_utils.update_file(file_path, album_string)
		except AssertionError:
			raise NotFoundException(album_path)

	logger.debug('Album [%s]: wrote to %s', album_path, file_path)


def get(album_path):
	"""
	Retrieve album from persistent store.

	Parameters
	----------
	album_path : string
		path of album, like '2005' or '2005/12-31'

	Return
	----------
	Album object

	Exception
	-----------
	Raises a NotFoundException if it can't find the album
	Raises an Exception if the retrieve fails for any reason.
	"""

	# get full path to album's JSON file on disk
	album_file_path = __file_path(album_path)

	# if album doesn't exist on disk, return None
	if not os.path.exists(album_file_path):
		raise NotFoundException(album_file_path)

	logger.debug('Album [%s]: reading from disk: %s', album_path, album_file_path)

	# get string of JSON from disk
	json_string = file_utils.read_file(album_file_path)

	# turn into Album object
	album = json_utils.from_string(json_string)

	if not album:
		raise AlbumException('Album [%s]: error retrieving from store, it is null' % album_path)

	if not isinstance(album, Album):
		raise AlbumException('Album [%s]: error retrieving from store, it is not an Album' % album_path)

	return album


def delete(album_path):
	"""
	Delete album from persistent store.

	Error if album does NOT exist.
	"""
	# raise exception if path is invalid
	album_utils.validate_album_path(album_path)

	# get full path to album's JSON file on disk
	album_file_path = __file_path(album_path)

	# if album doesn't exist on disk, return None
	if not os.path.exists(album_file_path):
		raise NotFoundException('Album [%s]: not found' % album_path)

	# delete album from disk
	file_utils.delete_file(album_file_path)


def __file_path(album_path):
	"""
	Return full path to album JSON file on disk

	Parameters
	----------
	albumPath : string
		path of album, like '2005' or '2005/12-31'

	Return
	----------
	Full path to album JSON file on disk
	"""

	# None or blank albumPath means it's the root album
	if not album_path:
		return os.path.join(config.ALBUM_DATA_DIR, 'album.json')
	else:
		return os.path.join(config.ALBUM_DATA_DIR, album_path, 'album.json')