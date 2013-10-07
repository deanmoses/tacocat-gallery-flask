import unittest, glob, time, os
import pycocat.album.utils.image_utils as image_utils
from pycocat.test.TestConfig import TestConfig

class TestImageUtils(unittest.TestCase):
	"""
	Tests using ImageMagick
	"""

	def get_pictures_expression(self):
		"""
		Expression to get a set of test pictures
		"""
		return os.path.join(TestConfig.image_bank_dir, '*.jpg')

	def test_get_dimensions_using_wand(self):
		"""
		Test getting the dimensions of some photos
		"""

		start_time = time.time()  # track how long it takes

		files = glob.glob(self.get_pictures_expression())
		self.assertTrue(len(files) > 0, 'No images matching this expression: ' + self.get_pictures_expression())
		for filename in files:
			width, height = image_utils.get_dimensions(filename=filename)
			print('%s: %sx%s' % (filename, width, height))
			self.assertTrue(width > 0, 'Width must be greater than 0')
			self.assertTrue(height > 0, 'Height must be greater than 0')

		end_time = time.time()
		duration = (end_time - start_time)
		print 'processed %s files in %0.3fs' % (len(files), duration)


	def test_get_dimensions_using_shell(self):
		"""
		Gets the dimensions of the same photos using subprocess instead of wand
		"""
		start_time = time.time()  # track how long it takes

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

		end_time = time.time()
		duration = (end_time - start_time)
		print 'processed files in %0.3fs' % duration