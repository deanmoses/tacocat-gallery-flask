"""
Read and write albums from disk
"""
import os
from pycocat.album.album_exceptions import FoundException

def create_file(album_path, album_string):
	"""
	Write specified string representing an Album to a file on disk.
	The string may be in XML or JSON or another format,
	it's not the job of this method to know.

	Parameters
	----------
	album_path : string
	   full file path + filename to where album should be written to disk

	album_string : string
		string representing an Album, will become contents of file on disk
	"""

	# make any of the parent dirs that haven't yet been created
	parent_dir = os.path.dirname(os.path.realpath(album_path))
	if not os.path.isdir(parent_dir): os.makedirs(parent_dir, 0755 )

	# error if file already exists
	assert not os.path.exists(album_path), "File already exists: %s" % album_path

	# write the file
	with open(album_path, "w+") as f:
		f.write(album_string)


def update_file(album_path, album_string):
	"""
	Write specified string representing an Album to a file on disk.
	The string may be in XML or JSON or another format,
	it's not the job of this method to know.

	Parameters
	----------
	albumPath : string
	   full file path + filename to where album should be written to disk

	albumString : string
		string representing an Album, will become contents of file on disk
	"""
	assert os.path.isfile(album_path), "File does not exist: %s" % album_path

	# write the file
	with open(album_path, "w+") as f:
		f.write(album_string)


def read_file(album_path):
	"""
	Retrieve album string from path
	"""
	with open(album_path) as f: return f.read()


def delete_file(album_path):
	"""
	Delete existing file on disk.
	Error if it doesn't exist
	"""
	os.remove(album_path)
	print 'deleted album from disk: %s' % album_path

	# remove directory if it is empty
	parent_dir = os.path.dirname(album_path)
	if not os.listdir(parent_dir):
		print 'removing empty dir: %s' % parent_dir
		os.rmdir(parent_dir)
