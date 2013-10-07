from pycocat.album.album_exceptions import ValidationException

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

class AlbumThumbnail(object):
	"""
	Just the info I need about an album to render a thumbnail with a title and link to the album.
	"""

	# My fields.  Do not include image because that's special
	__fields = ['path', 'publication_date', 'title', 'summary', 'height', 'width', 'url']

	def __init__(self):
		self.path = None  # "2001/12/31/someSubalbum"
		self.publication_date = None  # Unix timestamp of when this album was / will be published
		self.title = None  # "November 8"
		self.summary = None  # "First day of school"
		self.height = None
		self.width = None
		self.url = None


	def validate(self):
		"""
		Error if any of my fields are missing or invalid
		"""
		# ensure required fields aren't missing or blank
		for field_name in AlbumThumbnail.__fields:
			if (not hasattr(self, field_name)) or (not getattr(self, field_name)):
				raise ValidationException(field_name, "missing or blank")

		smallest_size = 100
		if int(self.height) < smallest_size:
			raise ValidationException('height', "%s is smaller than %s" % (self.height, smallest_size))
		if int(self.width) < smallest_size:
			raise ValidationException('width', "%s is smaller than %s" % (self.width, smallest_size))



	def to_dict(self):
		"""
		Create a dict from this object -- suitable for transforming into JSON or YAML.

		Skips any values that are None/blank/empty.
		"""
		d = {}
		# for all my fields
		for field_name in AlbumThumbnail.__fields:
			# add to dict if not None/blank/empty
			value = getattr(self, field_name)
			if value:
				d[field_name] = value

		return d


	@staticmethod
	def from_dict(d):
		"""
		Create object from a dict -- like when it comes from JSON or YAML.

		Ignores dict attrs that aren't valid object attrs
		"""
		object = AlbumThumbnail()

		# set non-required fields
		for field_name in AlbumThumbnail.__fields:
			try:
				setattr(object, field_name, d[field_name])
			except KeyError:
				pass

		return object