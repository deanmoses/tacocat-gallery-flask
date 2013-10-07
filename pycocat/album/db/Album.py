from pycocat.album.db.Photo import Photo
from pycocat.album.album_exceptions import PhotoNotFoundException

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

class Album(object):
	"""
	Represents the metadata for a photo album.  This is the source of truth.  Consider it a database.

	Does not contain any of the derived info, like my child albums
	"""

	# My fields.  Does not include photos field b/c that's special
	__fields = ['published', 'title', 'summary', 'description', 'thumbnail_photo', 'image_dir', 'photo_order']


	def __init__(self, title=None, summary=None, description=None, published=False):
		self.published = published # True: album is visible to non-admins
		self.title = title
		self.summary = summary
		self.description = description
		self.photos = {} # dict of 'felix1.jpg' -> Photo object
		self.photo_order = [] # Need only if photos aren't in alphabetical order
		self.thumbnail_photo = None # Logical path to thumb photo.  Could be in another album, especially a subalbum.  Example:  2001/12-31/felix.jpg
		self.image_dir = None # Absolute path to dir where my images are.  Only set if it's not the dir specified in Config.  Used for importing albums from elsewhere.  Example: ~/pix/2001/12/31/images


	def validate(self):
		for photo_name, photo_obj in self.photos.iteritems():
			photo_obj.validate()


	def to_dict(self):
		"""
		Create a dict from an album -- suitable for transforming into JSON or YAML.

		Skips any values that are None/blank/empty.
		"""
		d = {}
		# for all my fields
		for field_name in Album.__fields:
			# add to dict if not None/blank/empty
			value = getattr(self, field_name)
			if value:
				d[field_name] = value

		# add my photos if I have any
		if len(self.photos) > 0:
			d['photos'] = {}
			for photo_name, photo_value in self.photos.iteritems():
				d['photos'][photo_name] = photo_value.to_dict()

		return d


	@staticmethod
	def from_dict(d):
		"""
		Create Album from a dict -- like when it comes from JSON or YAML.

		Ignores dict attrs that aren't valid Album attrs
		"""
		album = Album()

		# set non-required fields
		for field_name in Album.__fields:
			try:
				setattr(album, field_name, d[field_name])
			except KeyError:
				pass

		# set photos
		if 'photos' in d:
			for photo_name, photo_value in d['photos'].iteritems():
				album.photos[photo_name] = Photo.from_dict(photo_value)

		return album


	def get_photo(self, photo_name):
		"""
		Return the specified photo
		"""
		try:
			return self.photos[photo_name]
		except KeyError:
			raise PhotoNotFoundException('Photo [%s] not found' % photo_name)

	def update_or_create_photo_from_dict(self, photo_name, photo_dict):
		"""
		Update the specified photo from a dict containing 'height' and 'width'
		"""
		photo = self.photos.get(photo_name)
		if photo:
			photo.update_from_dict(photo_dict)
		else:
			photo = Photo.from_dict(photo_dict)
			self.photos[photo_name] = photo


	def remove_photo(self, photo_name):
		"""
		Remove photo from my internal store.
		"""
		try:
			del self.photos[photo_name]
		except KeyError:
			raise PhotoNotFoundException('Photo [%s] not found' % photo_name)