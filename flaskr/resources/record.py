from flaskr.models import PersonRepository
from flaskr.db import session

from flask_restful import Resource


class RecordList(Resource):
    def get(self):
        pass

class Record(Resource):

    def get(self,id):
        pass

    def put(self,id):
        pass

    def delete(self,id):

        pass