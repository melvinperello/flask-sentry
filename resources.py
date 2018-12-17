from flask_restful import Resource
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from flask import request
#
from db import db,Person,Record,User
import time_provider

from flask_jwt_extended import jwt_required

#-------------------------------------------------------------------------------
# /person
#-------------------------------------------------------------------------------
'''

'''
class PersonAPI(Resource):
    json = {
            'id': fields.Integer,
            'type': fields.String,
            'nameLast': fields.String,
            'nameFirst': fields.String,
            'nameMiddle': fields.String,
            'nameExt' : fields.String,
            'contactTel' : fields.String,
            'contactMobile' : fields.String,
            'contactEmail' : fields.String,
            'updatedAt' : fields.Integer,
            'updatedBy' : fields.String,
        }
    
    def __init__(self):
        self.request_parser = reqparse.RequestParser()
        self.request_parser.add_argument('type', type=str,required=True,help='Type is required')
        self.request_parser.add_argument('nameLast', type=str,required=True,help='Last Name is required')
        self.request_parser.add_argument('nameFirst', type=str,required=True,help='First Name is required')
        self.request_parser.add_argument('nameMiddle', type=str)
        self.request_parser.add_argument('nameExt', type=str)
        self.request_parser.add_argument('contactTel', type=str)
        self.request_parser.add_argument('contactMobile', type=str)
        self.request_parser.add_argument('contactEmail', type=str)
        # end constructor
    
    @staticmethod
    def getActivePersonWithId(id):
        person = db.session.query(Person)\
                            .filter(Person.deletedAt == 0)\
                            .filter(Person.id == id)\
                            .first()
        if not person:
            abort(404, message="Person with id -- {} doesn't exist".format(id))
        return person
        
    pass # end class

class PersonListResource(PersonAPI):

    @marshal_with(PersonAPI.json)
    @jwt_required
    def get(self):
        personList = db.session.query(Person)\
                            .filter(Person.deletedAt == 0)\
                            .all()
        if not personList:
            abort(404, message="List is empty")
        return personList,200

    @marshal_with(PersonAPI.json)
    @jwt_required
    def post(self):
        parsed_args = self.request_parser.parse_args()

        person = Person()
        person.type = parsed_args['type']
        person.nameLast = parsed_args['nameLast']
        person.nameFirst = parsed_args['nameFirst']
        person.nameMiddle = parsed_args['nameMiddle']
        person.nameExt = parsed_args['nameExt']
        person.contactTel = parsed_args['contactTel']
        person.contactMobile = parsed_args['contactMobile']
        person.contactEmail = parsed_args['contactEmail']
        
        person.updatedAt = time_provider.getTime()
        person.updatedBy = 'SHawking:::Stephen Hawking'

        db.session.add(person)
        db.session.commit()
        return person,201


class PersonResource(PersonAPI):

    @marshal_with(PersonAPI.json)
    @jwt_required
    def get(self,id):
        return PersonAPI.getActivePersonWithId(id),200

    @marshal_with(PersonAPI.json)
    @jwt_required
    def put(self,id):
        parsed_args = self.request_parser.parse_args()
        
        person = PersonAPI.getActivePersonWithId(id)
        
        person.type = parsed_args['type']
        person.nameLast = parsed_args['nameLast']
        person.nameFirst = parsed_args['nameFirst']
        person.nameMiddle = parsed_args['nameMiddle']
        person.nameExt = parsed_args['nameExt']
        person.contactTel = parsed_args['contactTel']
        person.contactMobile = parsed_args['contactMobile']
        person.contactEmail = parsed_args['contactEmail']
        
        person.updatedAt = time_provider.getTime()
        person.updatedBy = 'JFNash:::John Forbes Nash'
        
        db.session.add(person)
        db.session.commit()
        return person, 200

    @jwt_required
    def delete(self,id):
        person = PersonAPI.getActivePersonWithId(id)
            
        person.deletedAt = time_provider.getTime()
        person.deletedBy = 'AEinstein:::Albert Einstein'
        
        db.session.add(person)
        db.session.commit()
        return {}, 204



#-------------------------------------------------------------------------------
# /record
#-------------------------------------------------------------------------------
class RecordAPI(Resource):
    json = {
        'id': fields.Integer,
        'type': fields.String,
        'timeIn': fields.Integer,
        'timeInBy': fields.String,
        'timeOut': fields.Integer,
        'timeOutBy': fields.String,
    }
    
    @staticmethod
    def getActivePersonWithId(person_id):
        return PersonAPI.getActivePersonWithId(person_id)
    
    @staticmethod
    def getActiveRecordWithId(id):
        record =  db.session.query(Record)\
                            .filter(Record.deletedAt == 0)\
                            .filter(Record.id == id)\
                            .first()
        if not record:
            abort(404, message="Record with id -- {} doesn't exist".format(id))
        return record
        
        
    pass # end class



class RecordPersonResource(RecordAPI):

    @marshal_with(RecordAPI.json)
    @jwt_required
    def get(self,person_id):
        records = db.session.query(Record)\
                            .filter(Record.deletedAt == 0)\
                            .filter(Record.person_id == person_id)\
                            .filter(Record.timeOut == 0)\
                            .all()
        return records
        
    # time in abort if already in
    @marshal_with(RecordAPI.json)
    @jwt_required
    def post(self,person_id):
        # Query all records with this person id, reject if there is a record with no time out
        # [abort] this person has a time in recod with no out record
        existRec = db.session.query(Record)\
                            .filter(Record.deletedAt == 0)\
                            .filter(Record.person_id == person_id)\
                            .filter(Record.timeOut == 0)\
                            .first()
        if existRec:
            abort(400, message="Person with id -- {} has already TIMED IN".format(id))
        # abort if person does not exist
        person = RecordAPI.getActivePersonWithId(person_id)
        # create record
        rec = Record()
        rec.person_id = person.id
        rec.type = person.type
        rec.timeIn = time_provider.getTime()
        rec.timeInBy = 'SHawking:::Stephen Hawking'
        # insert
        db.session.add(rec)
        db.session.commit()
        
        return rec, 201


class RecordResource(RecordAPI):
    @marshal_with(RecordAPI.json)
    @jwt_required
    def get(self,id):
        return RecordAPI.getActiveRecordWithId(id)
        
    # time out abort if already out
    @marshal_with(RecordAPI.json)
    @jwt_required
    def put(self,id):
        record = RecordAPI.getActiveRecordWithId(id)
        if record.timeOut != 0:
            abort(400, message="Record with id -- {} has already TIMED OUT".format(id))
        
        record.timeOut = time_provider.getTime()
        record.timeOutBy = 'JFNash:::John Forbes Nash'
        db.session.add(record)
        db.session.commit()
        return record, 200

    @jwt_required
    def delete(self,id):
        record = RecordAPI.getActiveRecordWithId(id)
        record.deletedAt = time_provider.getTime()
        record.deletedBy = 'AEinstein:::Albert Einstein'
        
        db.session.add(record)
        db.session.commit()
        return {}, 204
        
#-------------------------------------------------------------------------------
# /user
#-------------------------------------------------------------------------------
import uuid
import hashlib

class UserAPI(Resource):
    
    json = {
        'id': fields.Integer,
        'username': fields.String,
        'nameLast': fields.String,
        'nameFirst': fields.String,
        'nameMiddle': fields.String,
        'nameExt' : fields.String,
        'access' : fields.String,
        'updatedAt' : fields.Integer,
        'updatedBy' : fields.String,
    }
    
    def __init__(self):
        self.initPostParser()
        self.initLoginParser()
        # end constructor
        
    def initPostParser(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('username', type=str,required=True,help='Username is required')
        self.post_parser.add_argument('password', type=str)
        self.post_parser.add_argument('nameLast', type=str,required=True,help='Last Name is required')
        self.post_parser.add_argument('nameFirst', type=str,required=True,help='First Name is required')
        self.post_parser.add_argument('nameMiddle', type=str)
        self.post_parser.add_argument('nameExt', type=str)
        self.post_parser.add_argument('access', type=str,required=True,help='Access is required')
        
    def initLoginParser(self):
        self.login_parser = reqparse.RequestParser()
        self.login_parser.add_argument('username', type=str,required=True,help='Username is required')
        self.login_parser.add_argument('password', type=str,required=True,help='Password is required')
    
    @staticmethod
    def hash_password(password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()
        
    @staticmethod
    def getActiveUserWithId(id):
        user =  db.session.query(User)\
                            .filter(User.deletedAt == 0)\
                            .filter(User.id == id)\
                            .first()
        if not user:
            abort(404, message="User with id -- {} doesn't exist".format(id))
        return user
        
        
        
class UserListResource(UserAPI):
    @marshal_with(UserAPI.json)
    @jwt_required
    def get(self):
        userList = db.session.query(User)\
                            .filter(User.deletedAt == 0)\
                            .all()
        if not userList:
            abort(404, message="List is empty")
        return userList,200
        
    @marshal_with(UserAPI.json)
    @jwt_required
    def post(self):
        parsed_args = self.post_parser.parse_args()
        
        user = User()
        user.username = parsed_args['username']
        user.password = UserAPI.hash_password(parsed_args['password'])
        user.nameLast = parsed_args['nameLast']
        user.nameFirst = parsed_args['nameFirst']
        user.nameMiddle = parsed_args['nameMiddle']
        user.nameExt = parsed_args['nameExt']
        user.access = parsed_args['access']
        
        user.updatedAt = time_provider.getTime()
        user.updatedBy = 'SHawking:::Stephen Hawking'

        db.session.add(user)
        db.session.commit()
        return user,201
        
        
class UserResource(UserAPI):
    
    @marshal_with(UserAPI.json)
    @jwt_required
    def get(self,id):
        return UserAPI.getActiveUserWithId(id)
        
    # time out abort if already out
    @marshal_with(UserAPI.json)
    @jwt_required
    def put(self,id):
        user = UserAPI.getActiveUserWithId(id)
        
        parsed_args = self.post_parser.parse_args()
        user.username = parsed_args['username']
        # update password if not empty (change password)
        password = parsed_args['password']
        if password:
            user.password = UserAPI.hash_password(parsed_args['password'])
        #
        user.nameLast = parsed_args['nameLast']
        user.nameFirst = parsed_args['nameFirst']
        user.nameMiddle = parsed_args['nameMiddle']
        user.nameExt = parsed_args['nameExt']
        user.access = parsed_args['access']
        
        user.updatedAt = time_provider.getTime()
        user.updatedBy = 'JFNash:::John Forbes Nash'

        db.session.add(user)
        db.session.commit()
        return user, 200

    @jwt_required
    def delete(self,id):
        user = UserAPI.getActiveUserWithId(id)
        
        
        user.deletedAt = time_provider.getTime()
        user.deletedBy = 'AEinstein:::Albert Einstein'
        
        db.session.add(user)
        db.session.commit()
        return {}, 204

