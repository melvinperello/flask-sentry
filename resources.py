from flask_restful import Resource
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from flask import request
#
from db import db,Person,Record
import time_provider


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
        
        person.updatedAt = time_provider.getTime()
        person.updatedBy = 'SHawking:::Stephen Hawking'

        db.session.add(person)
        db.session.commit()
        return person,201


class PersonResource(PersonAPI):

    @marshal_with(PersonAPI.json)
    def get(self,id):
        return PersonAPI.getActivePersonWithId(id),200

    @marshal_with(PersonAPI.json)
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
    def get(self,person_id):
        records = db.session.query(Record)\
                            .filter(Record.deletedAt == 0)\
                            .filter(Record.person_id == person_id)\
                            .filter(Record.timeOut == 0)\
                            .all()
        return records
        
    # time in abort if already in
    @marshal_with(RecordAPI.json)
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
    def get(self,id):
        return RecordAPI.getActiveRecordWithId(id)
        
    # time out abort if already out
    @marshal_with(RecordAPI.json)
    def put(self,id):
        record = RecordAPI.getActiveRecordWithId(id)
        if record.timeOut != 0:
            abort(400, message="Record with id -- {} has already TIMED OUT".format(id))
        
        record.timeOut = time_provider.getTime()
        record.timeOutBy = 'JFNash:::John Forbes Nash'
        db.session.add(record)
        db.session.commit()
        return record, 200

    def delete(self,id):
        record = RecordAPI.getActiveRecordWithId(id)
        record.deletedAt = time_provider.getTime()
        record.deletedBy = 'AEinstein:::Albert Einstein'
        
        db.session.add(record)
        db.session.commit()
        return {}, 204