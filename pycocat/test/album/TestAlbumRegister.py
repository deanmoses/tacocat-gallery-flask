import unittest
from pycocat.album.AlbumService import AlbumService
from pycocat.Config import Config

class TestCompleteAlbumBuild(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		Config.test = True  # sets the location of the on-disk store of albums

	def test_register_album(self):
		"""
		Test building a CompleteAlbum from source files
		"""

		# have a year and a day test regular Albums ready to go: copy them from a static place
		year_path = "1960"
		day_path = "01-01"

		# register the album
		service = AlbumService()
		service.register_album(album_path)

		complete_album = get(year_path)

		# compare complete_album against gold file

		# delete the copied directories