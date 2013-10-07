import os, unittest, glob, shutil

from pycocat.album.AlbumService import AlbumService
from pycocat.album.album_exceptions import PhotoNotFoundException
from pycocat.Config import Config
from pycocat.test.TestConfig import TestConfig

class TestPhotoCreate(unittest.TestCase):
	"""
	Test creating and deleting photos
	"""

	year_path = '1964'  # year album to create
	day_path = year_path + '/01-01'  # week album to create
	service = AlbumService()


	@classmethod
	def setUpClass(cls):
		Config.test = True  # sets the location of the on-disk store of albums


	def setUp(self):

		# create fake year and week albums
		service = self.__class__.service
		year_path = self.__class__.year_path
		day_path = self.__class__.day_path

		service.create_album(year_path)
		service.create_album(day_path)



	def tearDown(self):

		# delete fake year and week albums
		service = self.__class__.service
		year_path = self.__class__.year_path
		day_path = self.__class__.day_path

		try:
			service.delete_album(day_path)
		except:
			pass

		try:
			service.delete_album(year_path)
		except:
			pass


	def test_create_photo(self):
		"""
		Test creating and deleting a photo
		"""
		service = self.__class__.service
		day_path = self.__class__.day_path

		# copy some test photos into the week album
		photo_names = self.add_photo_from_filesystem(day_path, 3)

		# register the photos in the album
		for photo_name in photo_names:
			# put photo's info into the album datafile
			service.register_photo(day_path, photo_name)

			# retrieve album and check that it has photo
			album = service.get_album(day_path)
			photo = album.get_photo(photo_name)
			self.assertIsNotNone(photo)
			self.assertGreater(photo.width, 100)
			self.assertGreater(photo.height, 100)

		# delete photos
		for photo_name in photo_names:
			# delete photo
			service.delete_photo(day_path, photo_name)

			# check that photo was deleted
			album = service.get_album(day_path)
			self.assertRaises(PhotoNotFoundException, album.get_photo, photo_name)


	def add_photo_from_filesystem(self, album_path, photo_count):
		"""
		Copy images from specified path into specified album.

		Returns name of the images
		"""

		photo_names = []

		# destination directory
		image_dest_dir = os.path.join(Config.album_data_dir(), album_path)
		for i in range(photo_count):
			# path to image file
			image_src_file = glob.glob(os.path.join(TestConfig.image_bank_dir, '*.jpg'))[i]
			# copy file
			shutil.copy(image_src_file, image_dest_dir)
			# add photo's name to list
			photo_names.append(os.path.basename(image_src_file))

		return photo_names



