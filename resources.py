from flask_restful import Resource
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from flask import request
#
from db import db,Person,Record
import time


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
        
    def getActivePersonWithId(self,id):
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
    def get(self):
        personList = db.session.query(Person)\
                            .filter(Person.deletedAt == 0)\
                            .all()
        if not personList:
            abort(404, message="List is empty")
        return personList,200

    @marshal_with(PersonAPI.json)
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
        
        person.updatedAt = time.time()
        person.updatedBy = 'sys'

        db.session.add(person)
        db.session.commit()
        return person,201


class PersonResource(PersonAPI):

    @marshal_with(PersonAPI.json)
    def get(self,id):
        return self.getActivePersonWithId(id),200

    @marshal_with(PersonAPI.json)
    def put(self,id):
        parsed_args = self.request_parser.parse_args()
        
        person = self.getActivePersonWithId(id)
        
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
        
        db.session.add(person)
        db.session.commit()
        return person, 201

    
    def delete(self,id):
        person = self.getActivePersonWithId(id)
            
        person.deletedAt = time.time()
        person.deletedBy = 'sys'
        
        db.session.add(person)
        db.session.commit()
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
        person = db.session.query(Person)\
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
        
        db.session.add(rec)
        db.session.commit()
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