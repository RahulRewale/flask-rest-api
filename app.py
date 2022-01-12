import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)

# upto SQLAlchemy 1.3 postgres and postgresql both were valid
# since SQLAlchemy 1.4, only postgresql works
# since Heroku's cold doesn't reflect this change yet, and it generates the database url for us, 
# which we cannot update, we need to handle this url issue in code as below
database_uri = os.getenv("DATABASE_URL", "sqlite:///data.db")
if database_uri.startswith("postgres://"):
	database_uri = database_uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'jeet'
api = Api(app)


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

# this below "__main__" code will not be executed on Heroku since we call uwsgi which internal executes our app
# on heroku, code in run.py file will be executed; to do this, in uwsgi.ini file we need to change module
if __name__ == '__main__': 
	from db import db
	db.init_app(app)

	if app.config['DEBUG']:
		@app.before_first_request
		def create_tables():
			db.create_all()
	
	app.run(port=5000, debug=True)