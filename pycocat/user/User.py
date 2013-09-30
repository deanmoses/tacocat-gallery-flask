import os
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
	def __init__(self, username):
		self.username = username

	def get_id(self):
		return self.username

	@staticmethod
	def _assert_valid_username(username):
		if username not in ['lucie', 'moses']: raise ValueError('name is not among allowed set')

	@staticmethod
	def _assert_valid_password(password):
		if not password: raise ValueError("password cannot be empty")
		if len(password) <= 5: raise ValueError("password must be longer than 5 characters")
		if '\n' in password: raise ValueError("password cannot contain newlines")

	@staticmethod
	def validate(username, password):
		User._assert_valid_username(username)
		User._assert_valid_password(password)

	@staticmethod
	def _user_file():
		return os.path.join(os.getcwd(), 'users.txt')

	#
	# Look up user from the user file
	#
	@staticmethod
	def get(username, password):
		# search for user line by line in the file,
		# stopping reading when it finds the user
		try:
			for line in open(User._user_file()):
				if username in line:
					salted_password = line.split('|')[1].rstrip('\n')
					if check_password_hash(salted_password, password):
						return User(username)
					return None
		except IOError:
			# file doesn't exist, so of course user's not in it
			pass

		return None

	@staticmethod
	def _user_exists(username):
		# search for user line by line in the file,
		# stopping reading when it finds the user
		try:
			for line in open(User._user_file()):
				if username in line:
					return True
		except IOError:
			# file doesn't exist, so of course user's not in it
			pass

		return False

	#
	# Create a user
	#
	@staticmethod
	def create(username, password):
		User.validate(username, password)

		# ensure user isn't already in file
		assert not User._user_exists(username)

		# encrypt password
		salted_password = generate_password_hash(password)

		# append user to the user file
		with open(User._user_file(), 'a') as f:
			f.write("%s|%s\n" % (username, salted_password))

