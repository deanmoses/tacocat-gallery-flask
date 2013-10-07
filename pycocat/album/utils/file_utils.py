"""
Read and write albums from disk
"""
import os, shutil

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

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


def create_or_overwrite_file(album_path, album_string):
	"""
	Write file to disk, regardless of whether it already exists or not.

	Errors if parent directories do not exist.
	"""
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
	logger.info('deleted album from disk: %s',  album_path)

	# remove directory if it is empty
	parent_dir = os.path.dirname(album_path)
	if not os.listdir(parent_dir):
		logger.info('removing empty dir: %s', parent_dir)
		os.rmdir(parent_dir)


def delete_dir(album_dir):
	"""
	Delete existing dir on disk
	"""
	shutil.rmtree(album_dir)
