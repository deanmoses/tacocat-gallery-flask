import unittest
from pycocat.imageUtils import get_dimensions
from os.path import expanduser, join
from glob import glob
from time import time

class TestImageUtils(unittest.TestCase):

	def test_get_dimensions(self):
		start_time = time()

		file_expression = join(expanduser('~'), 'Desktop') + '/*.jpg'
		files = glob(file_expression)
		self.assertTrue('No images in test dir', len(files) > 0)
		for filename in files:
			width, height = get_dimensions(filename=filename)
			print('%s: %sx%s' % (filename, width, height))
			self.assertTrue('Width greater than 0', width > 0)
			self.assertTrue('Height greater than 0', height > 0)

		end_time = time()
		duration = (end_time - start_time)
		print 'processed %s files in %0.3fs' % (len(files), duration)

	#
	# DOESN'T WORK YET
	#
	def test_get_dimensions_using_shell(self):
		start_time = time()

		from subprocess import call
		image_dir = join(expanduser('~'), 'Desktop')
		cmd = 'identify -format "\\n%f,%w,%h\\n" ' + image_dir + '/*.jpg'

		print cmd
		results = call('identify', '-format', '"\\n%f,%w,%h\\n"', image_dir + '/*.jpg')
		print(results)

		end_time = time()
		duration = (end_time - start_time)
		print 'processed files in %0.3fs' % (duration)