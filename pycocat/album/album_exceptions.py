class AlbumException(Exception):
	"""
	Base class for all exceptions in this package
	"""
	pass


class ValidationException(AlbumException):
	"""
	Raised when an Album or Photo isn't valid for saving
	"""
	def __init__(self, field, message):
		fullMessage = '%s is invalid: %s' % (field, message)

		# Call the base class constructor with the parameters it needs
		AlbumException.__init__(self, fullMessage)


class PathValidationException(AlbumException):
	"""
	Raised when path to an album or a photo isn't valid
	"""
	def __init__(self, path, message):
		full_message = '%s: %s' % (path, message)

		# Call the base class constructor with the parameters it needs
		AlbumException.__init__(self, full_message)


class NotFoundException(AlbumException):
	"""
	Raised when an Album or Photo isn't found
	"""
	pass


class FoundException(AlbumException):
	"""
	Raised when an Album or Photo is found and shouldn't be
	"""
	pass