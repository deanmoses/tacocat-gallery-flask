from store.AlbumStore import AlbumStore

#
# throws exception if save was not successful
# 
def save(path, attributes):
	
	# retrieve photo from persistent store
	photo = AlbumStore.getPhoto(path)

	# update the photo's fields
	changed = False
	for key, newvalue in attributes.iteritems():
		oldvalue = getattr(photo, key)
		if oldvalue != newvalue:
			setattr(photo, key, newvalue)
			changed = True	

			
	# todo: save photo
