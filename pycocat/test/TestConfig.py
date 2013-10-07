import os

class TestConfig(object):
	"""
	Configuration for tests
	"""

	test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data')
	image_bank_dir = os.path.join(test_data_dir, 'image_bank')



