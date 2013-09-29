



class Album(object):

	def __init__(self, path=None, title=None, summary=None):
		self.path = path
		self.title = title
		self.summary = summary

	def validate(self):
		Album.validate_path(self.path)
		Album.validate_title(self.title)
		Album.validate_summary(self.summary)

	def create(self):
		self.validate();
		raise NotImplementedError()

	def update(self):
		raise NotImplementedError()

	def delete(self):
		raise NotImplementedError()

	@staticmethod
	def validate_path(path):
		raise NotImplementedError()

	@staticmethod
	def validate_title(path):
		raise NotImplementedError()

	@staticmethod
	def validate_summary(path):
		raise NotImplementedError()
