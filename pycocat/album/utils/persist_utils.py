import os, glob, time, datetime

from pycocat.Config import Config
from pycocat.album.album_exceptions import AlbumException, FoundException, AlbumNotFoundException, PhotoNotFoundException, HasSubAlbumsException
from pycocat.album.utils import path_utils, image_utils, json_utils, file_utils
from pycocat.album.db.Album import Album
from pycocat.album.complete.CompleteAlbum import CompleteAlbum
from pycocat.album.complete.AlbumThumbnail import AlbumThumbnail

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)


def update(album_path, album):
	save(album_path, album, create=False)

def create(album_path, album):
	save(album_path, album, create=True)

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
			raise AlbumNotFoundException(album_path)

	logger.debug('Album [%s]: wrote to %s', album_path, file_path)

	__regenerate_complete_album(album_path, album)


def __regenerate_complete_album(album_path, db_album):

	album = CompleteAlbum.from_dict(db_album.to_dict())

	album.path = album_path

	#
	# generate sub album thumbs
	#
	sub_album_thumbs = []

	# get all my sub album data files
	for sub_file_path in glob.glob(__album_dir(album_path) + '/*/album.json'):
		# get logical path of sub album
		sub_path = __file_path_to_album_path(os.path.dirname(sub_file_path))
		# get dict of the sub album
		sub_album_d = get(sub_path).to_dict()
		# turn dict into thumb info
		sub_album_thumb = AlbumThumbnail.from_dict(sub_album_d)
		# add some derived fields
		sub_album_thumb.path = sub_path
		sub_album_thumb.publication_date = __path_to_timestamp(sub_album_thumb.path)

		sub_album_thumbs.append(sub_album_thumb)

	#
	# add derived info to my photos, like their URL
	#
	for photo_name, photo in album.photos.iteritems():
		photo.path = album_path + '/' + photo_name
		photo.url = Config.image_web_root()  + '/' + photo.path


	#
	# save CompleteAlbum
	#

	# raises exception if album has missing or invalid fields
	album.validate()

	# convert album object into JSON string
	album_string = json_utils.to_string(album)

	# get full path to album's JSON file on disk
	file_path = __complete_album_file_path(album_path)

	# write to disk
	file_utils.create_or_overwrite_file(file_path, album_string)

	logger.debug('CompleteAlbum [%s]: wrote to %s', album_path, file_path)



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
		raise AlbumNotFoundException(album_file_path)

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


def register_photo(album_path, photo_name):
		"""
		Look for specified photo on disk and add or update in album data file.
		"""

		# retrieve album first to ensure AlbumNotFound thrown before PhotoNotFound
		album = get(album_path)

		# file path to photo on disk
		photo_path = __photo_path(album_path, photo_name)
		if not os.path.isfile(photo_path):
			raise PhotoNotFoundException('Album [%s]: no such photo [%s]' % (album_path, photo_name))

		# get photo's height and width
		photo_dict = image_utils.get_info(photo_path)

		# update photo
		album.update_or_create_photo_from_dict(photo_name, photo_dict)

		# persist album
		update(album_path, album)


def delete_photo(album_path, photo_name):
	"""
	Delete the specified photo.
	"""

	# remove from album object
	album = get(album_path)
	album.remove_photo(photo_name)
	update(album_path, album)

	# remove from disk
	photo_path = __photo_path(album_path, photo_name)
	file_utils.delete_file(photo_path)


def __get_immediate_subdirs(dir):
	"""
	Return list of the specified directory's immediate subdirectories.
	"""
	return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]


def __has_subdirs(dir):
	"""
	True if the specified dir has immediate subdirs.
	"""
	subdirs = __get_immediate_subdirs(dir)
	return len(subdirs) > 0


def delete_album(album_path):
	"""
	Delete album from persistent store.

	Error if album does NOT exist, or album contains subalbums.
	"""
	# raise exception if path is invalid
	path_utils.validate_album_path(album_path)

	# full path to album dir on disk
	album_dir = __album_dir(album_path)

	# error if album doesn't exist on disk
	if not os.path.isdir(album_dir):
		raise AlbumNotFoundException('Album [%s]: not found' % album_path)

	# if album contains subalbums, raise exception

	if __has_subdirs(__album_dir(album_path)):
		raise HasSubAlbumsException('Album [%s]: has subdirectories, must delete those first' % album_path)

	# delete entire album directory from disk
	file_utils.delete_dir(album_dir)



def __photo_path(album_path, photo_name):
	"""
	Return full path to image file on disk
	"""
	return os.path.join(__album_dir(album_path), photo_name)


def __file_path(album_path):
	"""
	Return full path to album JSON file on disk

	Parameters
	----------
	album_path : string
		path of album, like '2005' or '2005/12-31'

	Return
	----------
	Full path to album JSON file on disk
	"""

	return os.path.join(__album_dir(album_path), 'album.json')


def __complete_album_file_path(album_path):
	return os.path.join(__album_dir(album_path), 'index.json')


def __album_dir(album_path):
	"""
	Return full directory file path to album on disk.
	"""

	# None or blank album_path means it's the root album
	if not album_path:
		return Config.album_data_dir()
	else:
		return os.path.join(Config.album_data_dir(), album_path)


def __file_path_to_album_path(file_path):
	"""
	Return the album path corresponding to the specified file path
	"""
	path = os.path.abspath(file_path)
	root = os.path.abspath(Config.album_data_dir())
	return path.replace(root, '')


def __path_to_timestamp(album_path):
	# convert path in to year, month day
	path_parts = path_utils.parent(album_path)
	year = path_parts[0]
	month = 1
	day = 1
	if len(path_parts) > 1:
		month_day = path_parts[1].split('-')
		month = month_day[0]
		day = month_day[1]

	# create date object
	date = datetime.date(year, month, day)

	# convert to timestamp
	return int(time.mktime(date))
