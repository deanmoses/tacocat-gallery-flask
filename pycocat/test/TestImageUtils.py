import unittest
from pycocat.imageUtils import get_dimensions
from os.path import expanduser, join
from glob import glob
from time import time

class TestImageUtils(unittest.TestCase):

	def get_pictures_expression(self):
		return join(expanduser('~'), 'Pictures', 'inbox', '*.jpg')

	def test_get_dimensions(self):
		start_time = time()  # track how long it takes

		files = glob(self.get_pictures_expression())
		self.assertTrue(len(files) > 0, 'No images matching this expression: ' + self.get_pictures_expression())
		for filename in files:
			width, height = get_dimensions(filename=filename)
			print('%s: %sx%s' % (filename, width, height))
			self.assertTrue(width > 0, 'Width must be greater than 0')
			self.assertTrue(height > 0, 'Height must be greater than 0')

		end_time = time()
		duration = (end_time - start_time)
		print 'processed %s files in %0.3fs' % (len(files), duration)

	#
	# DOESN'T WORK YET
	#
	def test_get_dimensions_using_shell(self):
		start_time = time()  # track how long it takes

		# get height and widths using shell script
		from subprocess import check_output
		results = check_output(['/usr/local/bin/identify', '-format', '%f:%w:%h\\n', self.get_pictures_expression()])

		for image_string in results.split('\n'):
			if image_string.strip():
				image_string_parts = image_string.split(':')
				name = image_string_parts[0]
				width = image_string_parts[1]
				height = image_string_parts[2]
				print("%s: %sx%s" % (name, width, height))

		end_time = time()
		duration = (end_time - start_time)
		print 'processed files in %0.3fs' % (duration)