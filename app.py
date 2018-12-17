# Create Flask Application
from flask import Flask, jsonify, request
app = Flask(__name__)

# Create Database Instance
from flask_sqlalchemy import SQLAlchemy
app.config.from_pyfile('sentry.cfg')
db = SQLAlchemy(app)

# Create API's Endpoint
from flask_restful import Api
api = Api(app)

# /person resources
from resources import PersonListResource,PersonResource
api.add_resource(PersonListResource, '/api/person') # GET (ALL) POST
api.add_resource(PersonResource,'/api/person/<int:id>') # GET PUT DELETE

# /record resources
from resources import RecordPersonResource,RecordResource
api.add_resource(RecordPersonResource, '/api/record/person/<int:person_id>') # GET (ALL) POST (Time In)
api.add_resource(RecordResource,'/api/record/<int:id>') # GET PUT (Time Out) DELETE (Cancel)

# /user resources
from resources import UserListResource,UserResource
api.add_resource(UserListResource, '/api/user') # POST (Add User)
api.add_resource(UserResource,'/api/user/<int:id>') # GET PUT (Update User) DELETE

# [middleware]
@app.after_request
def after_request(response):
    response.headers['SENTRY_NODE'] = 'sg-node-dev'
    return response

# [security]
from flask_jwt_extended import JWTManager,create_access_token
from resources import UserAPI
from db import User


jwt = JWTManager(app)

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/auth', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"message": "Missing username parameter"}), 400
    if not password:
        return jsonify({"message": "Missing password parameter"}), 400

    user =  db.session.query(User)\
            .filter(User.deletedAt == 0)\
            .filter(User.username == username)\
            .first()
            
    if not user:
        return jsonify({"message": "Username does not exists!"}), 400
    
    if UserAPI.check_password(user.password,password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Wrong password !"}), 400

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
    
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    
    return {
        'access': 'admin'
    }