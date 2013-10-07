import os

class Config(object):
	"""
	Configuration of paths and such
	"""
	test = False

	@staticmethod
	def album_data_dir():
		"""
		Root dir of the album JSON files on disk
		"""
		if Config.test:
			return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test', 'test_data', 'test_albums')
		else:
			return os.path.join(os.path.expanduser("~"), 'themosii.com', 'oldpix')

	@staticmethod
	def image_web_root():
		"""
		HTTP root of the image files
		"""
		if Config.test:
			return '/p'
		else:
			return '/oldpix'