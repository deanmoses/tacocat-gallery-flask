"""
Utilities for managing album paths
"""
from pycocat.album.album_exceptions import PathValidationException

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

def parse_path(album_path):
	"""
	Returns list of path components, throwing exception if path isn't valid

	Valid input formats:
	 2005
	 2005/12-31
	 2005/12-31/snuggery

	Parameters
	----------
	albumPath : string
		path of album, like '2005' or '2005/12-31'
		or '2005/12-31/snuggery'

	Returns
	----------
	list like ['2001', '12-31', 'snuggery']

	Raises
	----------
	PathValidationException if album is NOT a valid album path
	"""
	logger.debug('Parsing album or photo path: [%s]' % album_path)

	if not album_path: raise PathValidationException(album_path, 'cannot be empty')

	path_parts = album_path.split('/')
	if len(path_parts) > 4: raise PathValidationException(album_path, 'too many segments')

	#
	# validate year
	#
	year = path_parts.pop(0)
	if len(year) != 4: raise PathValidationException(album_path, 'invalid year')
	try:
		int(year)
	except ValueError:
		raise PathValidationException(album_path, 'invalid year')

	if len(path_parts) == 0:
		return [year]

	#
	# validate month-day
	#
	week = path_parts.pop(0)

	week_parts = week.split('-')
	if len(week_parts) != 2: raise PathValidationException(album_path, 'invalid week-day, too many or few dashes')

	#
	# validate month
	#
	month = week_parts.pop(0)
	if len(month) != 2: raise PathValidationException(album_path, 'invalid month')
	try:
		int(month)
	except ValueError:
		raise PathValidationException(album_path, 'invalid month')

	# validate day
	day = week_parts.pop(0)
	if len(day) != 2: raise PathValidationException(album_path, 'invalid day')
	try:
		int(day)
	except ValueError:
		raise PathValidationException(album_path, 'invalid day')

	if len(path_parts) == 0:
		return [year, week]

	photo_or_subalbum = path_parts.pop(0)
	if len(path_parts) == 0:
		return [year, week, photo_or_subalbum]

	subalbum = path_parts.pop(0)
	return [year, week, photo_or_subalbum, subalbum]


def validate_album_path(album_path):
	"""
	Raise error if it isn't a valid album path
	"""
	parse_path(album_path)


def validate_photo_path(photo_path):
	"""
	Raise error if it isn't a valid photo path
	"""
	if len(parse_path(photo_path)) < 3:
		raise PathValidationException(photo_path, 'no photo on path')


def parent(child_path):
	"""
	Get the parent path.  Examples:
	2005/12-31 -> 2005
	2005/12-31/felix.jpg -> 2005/12-31
	2005/12-31/snuggery -> 2005/12-31
	"""
	path_list = parse_path(child_path)
	path_list.pop()
	return '/'.join(path_list)