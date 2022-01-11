from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'jeet'
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
	db.create_all()


jwt = JWT(app, authenticate, identity)	# creates a new endpoint /auth

# items = []

# class Item(Resource):

# 	parser = reqparse.RequestParser()
# 	parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')

# 	@jwt_required()
# 	def get(self, name):
# 		# for item in items:
# 		# 	if item['name'] == name:
# 		# 		return item
# 		# return {'item': None}, 404
		
# 		# succinct version of the above code
# 		item = next(filter(lambda x: x['name'] == name, items), None)
# 		return {'item': item}, 200 if item else 404

		

# 	def post(self, name):
# 		if next(filter(lambda x: x['name'] == name, items), None):	# item already exists
# 			return {'message': f'Item with name {name} already exists'}, 400

# 		data = request.get_json()
# 		item = {'name': name, 'price': data['price']}
# 		items.append(item)
# 		return item, 201

 
# 	def delete(self, name):
# 		global items
# 		items = list(filter(lambda x: x['name'] != name, items))
# 		return {'message': 'Item deleted'}


# 	def put(self, name):

# 		# data = request.get_json()
# 		item = next(filter(lambda x: x['name'] == name, items), None)
		
# 		data = Item.parser.parse_args()

# 		if item:
# 			item.update(data)	# using dictionary update() method
# 			# using update() updates all fields, including name, in item with the values in data
# 			# to limit the fields that are updated, use reqparse
			
# 		else:
# 			item = {'name': name, 'price': data['price']}
# 			items.append(item)

# 		return item

# class ItemList(Resource):

# 	def get(self):
# 		return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
	# db.init_app(app)
	app.run(port=5000, debug=True)
