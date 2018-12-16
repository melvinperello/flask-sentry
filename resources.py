
# rest
from flask_restful import Resource
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
# request
from flask import request

import time


from app import app
from models import Person
from models import Record
# db
from db import session

@app.teardown_request
def remove_session(ex=None):
    print("session_removed")
    session.remove()



#-------------------------------------------------------------------------------
# /person
#-------------------------------------------------------------------------------
personParser = reqparse.RequestParser()
personParser.add_argument('type', type=str,required=True,help='Type is required')
personParser.add_argument('nameLast', type=str,required=True,help='Last Name is required')
personParser.add_argument('nameFirst', type=str,required=True,help='First Name is required')
personParser.add_argument('nameMiddle', type=str)
personParser.add_argument('nameExt', type=str)
personParser.add_argument('contactTel', type=str)
personParser.add_argument('contactMobile', type=str)
personParser.add_argument('contactEmail', type=str)

personFields = {
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
class PersonListResource(Resource):

    @marshal_with(personFields)
    def get(self):
        personList = session.query(Person)\
                            .filter(Person.deletedAt == None)\
                            .all()
        if not personList:
            abort(404, message="List is empty")
        return personList,200

    @marshal_with(personFields)
    def post(self):
        parsed_args = personParser.parse_args()

        person = Person()
        person.type = parsed_args['type']
        person.nameLast = parsed_args['nameLast']
        person.nameFirst = parsed_args['nameFirst']
        person.nameMiddle = parsed_args['nameMiddle']
        person.nameExt = parsed_args['nameExt']
        person.contactTel = parsed_args['contactTel']
        person.contactMobile = parsed_args['contactMobile']
        person.contactEmail = parsed_args['contactEmail']
        
        person.updatedAt = time.time()
        person.updatedBy = 'sys'

        session.add(person)
        session.commit()
        return person,201


class PersonResource(Resource):

    @marshal_with(personFields)
    def get(self,id):
        person = session.query(Person)\
                        .filter(Person.deletedAt == 0)\
                        .filter(Person.id == id)\
                        .first()
        if not person:
            abort(404, message="Person {} doesn't exist".format(id))
        return person,200

    @marshal_with(personFields)
    def put(self,id):
        parsed_args = personParser.parse_args()
        
        person = session.query(Person)\
                        .filter(Person.deletedAt == 0)\
                        .filter(Person.id == id)\
                        .first()
        if not person:
            abort(404, message="Person {} doesn't exist".format(id))
        
        person.type = parsed_args['type']
        person.nameLast = parsed_args['nameLast']
        person.nameFirst = parsed_args['nameFirst']
        person.nameMiddle = parsed_args['nameMiddle']
        person.nameExt = parsed_args['nameExt']
        person.contactTel = parsed_args['contactTel']
        person.contactMobile = parsed_args['contactMobile']
        person.contactEmail = parsed_args['contactEmail']
        
        person.updatedAt = time.time()
        person.updatedBy = 'sys_update'
        
        session.add(person)
        session.commit()
        return person, 201

    
    def delete(self,id):
        person = session.query(Person)\
                        .filter(Person.deletedAt == 0)\
                        .filter(Person.id == id)\
                        .first()
        if not person:
            abort(404, message="Person {} doesn't exist".format(id))
            
        person.deletedAt = time.time()
        person.deletedBy = 'sys'
        
        session.add(person)
        session.commit()
        return {}, 204



#-------------------------------------------------------------------------------
# /record
#-------------------------------------------------------------------------------
recordFields = {
    'id': fields.Integer,
    'type': fields.String,
}

class RecordPersonResource(Resource):
    def get(self,person_id):
        pass
    
    @marshal_with(recordFields)
    def post(self,person_id):
        person = session.query(Person)\
                        .filter(Person.deletedAt == 0)\
                        .filter(Person.id == person_id)\
                        .first()
                        
        if not person:
            abort(404, message="Person {} doesn't exist".format(id))
            
        #
        rec = Record()
        rec.person_id = person.id
        rec.type = person.type
        
        rec.timeIn = time.time()
        
        rec.updatedAt = time.time()
        rec.updatedBy = 'sys'
        
        session.add(rec)
        session.commit()
        return rec, 201

class RecordListResource(Resource):
    def get(self):
        pass

class RecordResource(Resource):

    def get(self,id):
        pass

    def put(self,id):
        pass

    def delete(self,id):

        pass