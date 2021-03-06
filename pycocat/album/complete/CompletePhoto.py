from pycocat.album.album_exceptions import ValidationException

class CompletePhoto(object):
	"""
	Represents everything needed for a complete photo ready to be sent back as JSON to the client.

	This will contain derived information that's not in the actual photo file, such as the photo's dimensions.
	"""

	# My fields
	__fields = ['path', 'title', 'description', 'height', 'width', 'url']


	def __init__(self, title=None, description=None):
		self.title = title  # title of photo
		self.description = description  # caption of photo, often contains HTML


	def validate(self):
		"""
		Error if any of my fields are missing or invalid
		"""
		# ensure required fields aren't missing or blank
		for field_name in ['title']:
			if (not hasattr(self, field_name)) or (not getattr(self, field_name)):
				raise ValidationException(field_name, "missing or blank")



	def to_dict(self):
		"""
		Create a dict from an album -- suitable for transforming into JSON or YAML.

		Skips any values that are None/blank/empty.
		"""
		d = {}
		# for all my fields
		for field_name in CompletePhoto.__fields:
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
		photo = CompletePhoto()

		# set non-required fields
		for field_name in CompletePhoto.__fields:
			try:
				setattr(photo, field_name, d[field_name])
			except KeyError:
				pass

		return photo


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