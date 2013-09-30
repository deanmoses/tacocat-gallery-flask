import album_utils
from Photo import Photo

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

class Album(object):
	"""
	Represents the metadata for a photo album.
	"""

	# My fields.  Does not include photos field b/c that's special
	__fields = ['published', 'title', 'summary', 'description', 'thumbnail_photo', 'image_dir', 'photo_order']

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
		try:
			for photo_name, photo_value in d['photos']:
				album.photos[photo_name] = Photo.from_dict(photo_value)
		except KeyError:
				pass

		return album


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
			for photo_name, photo_value in self.photos:
				d['photos'][photo_name] = photo_value.to_dict()

		return d


	def __init__(self, title=None, summary=None, description=None, published=False):
		self.published = published # True: album is visible to non-admins
		self.title = title
		self.summary = summary
		self.description = description
		self.photos = {} # dict of 'felix1.jpg' -> Photo object
		self.photo_order = [] # Need only if photos aren't in alphabetical order
		self.thumbnail_photo = None # Logical path to thumb photo.  Could be in another album, especially a subalbum.  Example:  2001/12-31/felix.jpg
		self.image_dir = None # Absolute path to dir where my images are.  Only set if it's not the dir specified in Config.  Used for importing albums from elsewhere.  Example: ~/pix/2001/12/31/images

	def create(self):
		album_utils.save(self, create=True)

	def update(self):
		album_utils.save(self, create=False)

	def delete(self):
		raise NotImplementedError()

	def validate(self):
		pass