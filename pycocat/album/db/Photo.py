from pycocat.album.album_exceptions import ValidationException

class Photo(object):
	"""
	A photo in an Album
	"""

	# My fields
	__fields = ['description','height','width']


	def __init__(self, description=None, height=None, width=None):
		self.description = description  # caption of photo, often contains HTML
		self.height = None  # height of photo in px
		self.width = None  # width of photo in px

		if height:
			self.height = long(height)

		if width:
			self.width = long(width)


	def validate(self):
		"""
		Error if any of my fields are missing or invalid
		"""
		smallest_size = 100
		if long(self.height) < smallest_size:
			raise ValidationException('height', "%s is smaller than %s" % (self.height, smallest_size))
		if long(self.width) < smallest_size:
			raise ValidationException('width', "%s is smaller than %s" % (self.width, smallest_size))


	def to_dict(self):
		"""
		Create a dict from an album -- suitable for transforming into JSON or YAML.

		Skips any values that are None/blank/empty.
		"""
		d = {}
		# for all my fields
		for field_name in Photo.__fields:
			# add to dict if not None/blank/empty
			value = getattr(self, field_name)
			if value:
				d[field_name] = value
		return d


	@staticmethod
	def from_dict(d):
		"""
		Create Photo from a dict -- like when it comes from JSON or YAML.

		Ignores dict attrs that aren't valid Photo attrs
		"""
		photo = Photo()
		photo.update_from_dict(d)
		return photo


	def update_from_dict(self, d):
		"""
		Update the photo from the dict
		"""
		for field_name in Photo.__fields:
			try:
				setattr(self, field_name, d[field_name])
			except KeyError:
				pass


	def __str__(self):
		"""
		Python's built-in toString() method
		"""
		return str(self.__dict__)


	def __eq__(self, other):
		"""
		Python's built-in equality comparison
		"""
		return self.__dict__ == other.__dict__