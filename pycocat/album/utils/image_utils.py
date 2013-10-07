#
# Utilities for reading and manipulating images
#
from wand.image import Image
import string, re


def get_dimensions(filename):
	"""Returns tuple of height,width"""
	with Image(filename=filename) as img:
		return img.width, img.height


def get_info(filename):
	"""
	Return dict of info about photo, such as width and height
	"""
	with Image(filename=filename) as img:
		return {
			'width': img.width,
			'height': img.height
		}


def pretty_title(filename):
	"""
	Turn filename into a pretty title
	"""

	if not filename:
		return ''

	title = filename.strip()

	# remove numbers from the start of the title,
	# they seem to always be used to order a set of photos
	# turn 10sea-horses into sea-horses
	# turn 01-julie into -julie
	title = re.sub(r'^(\d+)', r'', title)

	# replace dashes and underscores with spaces
	title = title.replace('_', ' ').replace('-', ' ').strip()

	# do title capitalization
	title = string.capwords(title)

	# humanize numbers at the end of the title
	# turn Christmas Supper01 into Christmas Supper 1
	# turn Track 0 into Track
	def process_end_number(match):
		match = match.group()
		num = int(match)
		if num == 0:
			return ''
		else:
			return ' %s' % int(match)

	#title = re.sub(r'(\d+)$', r' \1', title)
	title = re.sub(r'(\d+)$', process_end_number, title)

	# turn Felixs into Felix's
	names = ['Dean', 'Lucie', 'Felix', 'Milo', 'Nana', 'Austin', 'Mike']
	for name in names:
		expression1 = name + 's '
		expression2 = name + "'s "
		title = re.sub(str(expression1), str(expression2), title)

	# get rid of two spaces in a row
	title = title.replace('  ', ' ')

	# sanity check that all front and rear space is gone
	title = title.strip()

	return title