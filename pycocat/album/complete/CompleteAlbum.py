from CompletePhoto import CompletePhoto
from AlbumThumbnail import AlbumThumbnail

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

class CompleteAlbum(object):
	"""
	Represents everything needed for a complete photo album ready to be sent back as JSON to the client.

	This will contain derived information that's not in the actual album, like sub album thumbnails.
	"""

	# My fields.  Does not include photos or subalbum_thumbs fields b/c they're special
	__fields = ['path', 'published', 'publication_date', 'title', 'summary', 'description', 'thumbnail_photo', 'image_dir', 'photo_order']

	def __init__(self, path=None, title=None, summary=None, description=None, published=False):
		self.path = path  # full path like 2008/12-31
		self.published = published  # True: album is visible to non-admins
		self.publication_date  = None  # Unix timestamp of when this album was / will be published
		self.title = title
		self.summary = summary
		self.description = description
		self.photos = {}  # dict of 'felix1.jpg' -> Photo object
		self.photo_order = []  # Need only if photos aren't in alphabetical order
		self.thumbnail_photo = None  # Logical path to thumb photo.  Could be in another album, especially a subalbum.  Example:  2001/12-31/felix.jpg
		self.image_dir = None  # Absolute path to dir where my images are.  Only set if it's not the dir specified in Config.  Used for importing albums from elsewhere.  Example: ~/pix/2001/12/31/images
		self.subalbum_thumbs = {}  # dict of '12-31' -> AlbumThumbnail object


	def validate(self):
		pass


	def to_dict(self):
		"""
		Create a dict from an album -- suitable for transforming into JSON or YAML.

		Skips any values that are None/blank/empty.
		"""
		d = {}
		# for all my fields
		for field_name in CompleteAlbum.__fields:
			# add to dict if not None/blank/empty
			value = getattr(self, field_name)
			if value:
				d[field_name] = value

		# add my photos if I have any
		if len(self.photos) > 0:
			d['photos'] = {}
			for photo_name, photo_value in self.photos.iteritems():
				d['photos'][photo_name] = photo_value.to_dict()

		# add my subalbum thumbnails if I have any
		if len(self.subalbum_thumbs) > 0:
			d['subalbum_thumbs'] = {}
			for album_name, album_value in self.subalbum_thumbs.iteritems():
				d['subalbum_thumbs'][album_name] = album_value.to_dict()

		return d


	@staticmethod
	def from_dict(d):
		"""
		Create Album from a dict -- like when it comes from JSON or YAML.

		Ignores dict attrs that aren't valid Album attrs
		"""
		album = CompleteAlbum()

		# set non-required fields
		for field_name in CompleteAlbum.__fields:
			try:
				setattr(album, field_name, d[field_name])
			except KeyError:
				pass

		# set photos
		try:
			for photo_name, photo_value in d['photos'].iteritems():
				album.photos[photo_name] = CompletePhoto.from_dict(photo_value)
		except KeyError:
			pass

		# set albums
		try:
			for album_name, album_value in d['subalbum_thumbs'].iteritems():
				album.subalbum_thumbs[album_name] = AlbumThumbnail.from_dict(album_value)
		except KeyError:
			pass

		return album