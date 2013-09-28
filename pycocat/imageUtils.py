#
# Utilities for reading and manipulating images
#
from wand.image import Image

def get_dimensions(filename):
	"""Returns tuple of height,width"""
	with Image(filename=filename) as img:
		return img.width, img.height