import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
	parser.add_argument('store_id', type=int, required=True, help='Every item needs a store id')

	@jwt_required() 
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()

		return {'message': 'Item not found'}, 404
		

	def post(self, name):

		# if next(filter(lambda x: x['name'] == name, items), None):	# item already exists
		# 	return {'message': f'Item with name {name} already exists'}, 400

		if ItemModel.find_by_name(name):
			return {'message': f'Item with name {name} already exists'}, 400

		# data = request.get_json()
		data = Item.parser.parse_args()
		# item = {'name': name, 'price': data['price']}
		item = ItemModel(name, data['price'], data['store_id'])

		try:
			# ItemModel.insert(item)
			# item.insert()
			item.save_to_db()
		except Exception as e:
			return {"message": "An error occurred while inserting the item."}, 500	# Internal Server Error

		return item.json(), 201


	def delete(self, name):
		
		# connection = sqlite3.connect("data.db")
		# cursor = connection.cursor()

		# cursor.execute("DELETE FROM items WHERE name=?", (name, ))

		# connection.commit()
		# connection.close()

		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item deleted'}


	def put(self, name):

		# data = request.get_json()
		data = Item.parser.parse_args()

		# item = next(filter(lambda x: x['name'] == name, items), None)
		item = ItemModel.find_by_name(name)
		
		# updated_item = {'name': name, 'price': data['price']}
		# updated_item = ItemModel(name, data['price'])

		if item:
			item.price = data['price']
			# try:
			# 	updated_item.update()
			# except Exception as e:
			# 	print(e)
			# 	return {"message": "An error occurred while updating the item"}, 500
		else:
			# try:
			# 	updated_item.insert()
			# except Exception as e:
			# 	print(e)
			# 	return {"message": "An error occurred while inserting the item"}, 500
			item = ItemModel(name, data['price'], data['store_id'])

		# return updated_item.json()
		item.save_to_db()
		return item.json()

	

class ItemList(Resource):

	def get(self):
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		# result = cursor.execute("SELECT * from items")

		# items = []
		# for row in result:
		# 	items.append({"name": row[0], "price": row[1]})

		# connection.close()

		# return {'items': items}
		
		return {'items': [item.json() for item in ItemModel.query.all()]} 
		# OR use below
		# return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
