from pycocat.album.db.Album import Album
from pycocat.album.utils import persist_utils

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

class AlbumService(object):
	"""
	Public interface to albums and photos.
	"""

	def __init__(self):
		pass

	def create_album(self, album_path, title=None, summary=None, description=None):
		"""
		Create new album in persistent store.

		Error if album already exists.
		"""
		album = Album(title=title, summary=summary, description=description)
		return persist_utils.save(album_path, album, create=True)


	def get_album(self, album_path):
		"""
		Retrieve specified album from persistent store.

		Error if album does not exist.
		"""
		return persist_utils.get(album_path)


	def delete_album(self, album_path):
		"""
		Delete album from disk.

		Error if album does NOT exist.
		"""
		return persist_utils.delete_album(album_path)


	def register_photo(self, album_path, photo_name):
		"""
		Look for specified photo on disk and add or update in album data file.

		Call this after uploading a photo to register it in the album.
		"""
		return persist_utils.register_photo(album_path, photo_name)


	def delete_photo(self, album_path, photo_name):
		"""
		Delete the specified photo.
		"""
		persist_utils.delete_photo(album_path, photo_name)
