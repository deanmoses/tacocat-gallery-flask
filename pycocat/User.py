__author__ = 'dmoses'

from flask.ext.login import UserMixin

class User(UserMixin):

	def __init__(self):
		self._username = None
		self._password = None

	@property
	def username(self):
		'''Username property'''
		return self._username

	@property
	def password(self):
		'''Password property'''
		return self._password

	def get_id(self):
		return self.username

	#
	# TODO: actually implement a real user lookup
	#
	@staticmethod
	def get(username):
		return User(username)