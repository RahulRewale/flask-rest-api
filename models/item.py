# import sqlite3
from db import db


class ItemModel(db.Model):

	__tablename__ = 'items'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=2))	# precision - 2 digits after decimal point

	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
	store = db.relationship('StoreModel')


	def __init__(self, name, price, store_id):
		self.name = name
		self.price = price
		self.store_id = store_id

	def json(self):
		return {'name': self.name, 'price': self.price}

	@classmethod
	def find_by_name(cls, name):
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		# items = cursor.execute("SELECT * from items WHERE name=?", (name,))
		# row = items.fetchone()
		# connection.close()
		# if row:
		# 	return cls(*row)
		return cls.query.filter_by(name=name).first()
		# SELECT * FROM items WHERE name=name LIMIT 1

	# def insert(self):
	# 	# connection = sqlite3.connect("data.db")
	# 	# cursor = connection.cursor()
	# 	# cursor.execute("INSERT INTO items VALUES(?, ?)", (self.name, self.price))
	# 	# connection.commit()
	# 	# connection.close()

	# def update(self):
	# 	connection = sqlite3.connect("data.db")
	# 	cursor = connection.cursor()
	# 	cursor.execute("UPDATE items SET price=? WHERE name=?", (self.price, self.name))
	# 	connection.commit()
	# 	connection.close()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()