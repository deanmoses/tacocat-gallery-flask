import unittest

from pycocat.album.AlbumService import AlbumService
from pycocat.album.album_exceptions import AlbumNotFoundException, HasSubAlbumsException
from pycocat.Config import Config

class TestAlbumCreate(unittest.TestCase):
	"""
	Test album creation and deletion
	"""

	year_path = '1963'  # year album to create
	day_path = year_path + '/01-01'  # week album to create
	service = AlbumService()


	@classmethod
	def setUpClass(cls):
		Config.test = True  # sets the location of the on-disk store of albums


	def tearDown(self):
		service = AlbumService()

		try:
			service.delete_album(self.__class__.day_path)
		except:
			pass

		try:
			service.delete_album(self.__class__.year_path)
		except:
			pass


	def test_create_album(self):
		"""
		Test creating and deleting albums and photos
		"""

		service = TestAlbumCreate.service

		# create a fake year album
		year_path = TestAlbumCreate.year_path
		self.assert_album_not_exists(year_path)
		service.create_album(year_path)
		self.assert_album_exists(year_path)

		# create a fake week album under the year
		day_path = TestAlbumCreate.day_path
		self.assert_album_not_exists(day_path)
		service.create_album(day_path)
		self.assert_album_exists(day_path)

		# should NOT be able to delete an album that has subalbums
		self.assertRaises(HasSubAlbumsException, service.delete_album, year_path)

		# delete fake day album
		service.delete_album(day_path)
		self.assert_album_not_exists(day_path)

		# delete fake year album
		service.delete_album(year_path)
		self.assert_album_not_exists(year_path)


	def assert_album_exists(self, album_path):
		album = TestAlbumCreate.service.get_album(album_path)
		self.assertIsNotNone(album, 'Album [%s] should exist' % album_path)

	def assert_album_not_exists(self, album_path):
		self.assertRaises(AlbumNotFoundException, TestAlbumCreate.service.get_album, album_path)


