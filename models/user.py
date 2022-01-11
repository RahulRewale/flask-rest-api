import sqlite3
from db import db


class UserModel(db.Model):

	# DB table name
	__tablename__ = 'users'

	# columns in the table; SQLAlchemy will deal with this columns only in the 'users' table.
	# below variable names must match exactly with the object attributes that we have defined 
	# in __init__() method
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))

	# note: we are using _id because id is a python in-built function
	def __init__(self, username, password):		# removed _id parameter
		# self.id = _id 						# no longer required when using SQLAlchemy
		self.username = username
		self.password = password
		# you can have additional attributes in your class that don't map to any column in the table
		# self.something = "something"	

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def find_by_username(cls, username):
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()

		# query = "SELECT * FROM users WHERE username=?"
		# result = cursor.execute(query, (username,))	# parameters always have to be in form of a tuple
		# row = result.fetchone()

		# if row:
		# 	user = cls(*row)	# unpacking row[0], row[1], and row[2]
		# else:
		# 	user = None

		# connection.close()
		# return user

		return cls.query.filter_by(username=username).first()

	@classmethod
	def find_by_id(cls, _id):	
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()

		# query = "SELECT * FROM users WHERE id=?"
		# result = cursor.execute(query, (_id,))	# parameters always have to be in form of a tuple
		# row = result.fetchone()

		# if row:
		# 	user = cls(*row)	# unpacking row[0], row[1], and row[2]
		# else:
		# 	user = None

		# connection.close()
		# return user
		return cls.query.filter_by(id=_id).first()
