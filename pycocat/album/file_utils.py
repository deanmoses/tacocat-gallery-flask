"""
Read and write albums from disk
"""
import os

def create_file(albumPath, albumString):
	'''
	Write specified string representing an Album to a file on disk.
	The string may be in XML or JSON or another format,
	it's not the job of this method to know.

	Parameters
	----------
	albumPath : string
	   full file path + filename to where album should be written to disk

	albumString : string
		string representing an Album, will become contents of file on disk
	'''
	# make any of the parent dirs that haven't yet been created
	parentDir = os.path.dirname(os.path.realpath(albumPath))
	if not os.path.isdir(parentDir): os.makedirs(parentDir, 0755 )

	# write the file
	with open(albumPath, "w+") as f:
	    f.write(albumString)


def update_file(albumPath, albumString):
	'''
	Write specified string representing an Album to a file on disk.
	The string may be in XML or JSON or another format,
	it's not the job of this method to know.

	Parameters
	----------
	albumPath : string
	   full file path + filename to where album should be written to disk

	albumString : string
		string representing an Album, will become contents of file on disk
	'''
	assert os.path.isfile(albumPath), "File does not exist: %s" % albumPath

	# write the file
	with open(albumPath, "w+") as f:
	    f.write(albumString)


def read_file(albumPath):
	"""
	Retrieve album string from path
	"""
	with open(albumPath) as f: return f.read()


def delete_file(albumPath):
	"""
	Delete existing file on disk.
	Error if it doesn't exist
	"""
	os.remove(albumPath)
	print 'deleted album from disk: %s' % albumPath

	# remove directory if it is empty
	parentDir = os.path.dirname(albumPath)
	if not os.listdir(parentDir):
		print 'removing empty dir: %s' % parentDir
		os.rmdir(parentDir)
