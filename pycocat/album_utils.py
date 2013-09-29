from Album import Album


#
# Utilities for accessing Albums
#

def create_album(albumPath, title, summary):

	# instantiate album object, set fields
	# album.validate() will validate path, title, summary
	# create album on disk
	# catch error if it already exists and return nice
	album = Album(albumPath, title, summary)
	album.create()