class AlbumException(Exception):
	"""
	Base class for all exceptions in this package.
	"""
	pass


class ValidationException(AlbumException):
	"""
	Raised when an Album or Photo isn't valid for saving
	"""
	def __init__(self, field, message):
		full_message = '%s is invalid: %s' % (field, message)

		# Call the base class constructor with the parameters it needs
		AlbumException.__init__(self, full_message)


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
	Base class for album and photo not found exceptions
	"""
	pass


class AlbumNotFoundException(NotFoundException):
	"""
	Raised when an Album isn't found
	"""
	pass

class PhotoNotFoundException(NotFoundException):
	"""
	Raised when a Photo isn't found
	"""
	pass

class FoundException(AlbumException):
	"""
	Base class for album and photo found exceptions
	"""
	pass

class AlbumFoundException(FoundException):
	"""
	Raised when an Album is found and shouldn't
	"""
	pass

class PhotoFoundException(FoundException):
	"""
	Raised when a Photo is found and shouldn't
	"""
	pass

class HasSubAlbumsException(AlbumException):
	"""
	Raised when an album shouldn't have subalbums but does, like when
	we're asked to delete it.
	"""
	pass