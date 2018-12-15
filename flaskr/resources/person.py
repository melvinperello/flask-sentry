from flask_restful import Resource


class PersonList(Resource):
    def get(self):
        return "hello"
        pass

    def post(self):
        # create new person
        pass


class Person(Resource):
    def get(self,id):
        return "hi" + " " + id
        pass

    def put(self,id):
        # update
        pass

    def delete(self,id):
        # delete
        pass

class PersonRecordList(Resource):

    def get(self,person_id):
        # get all records of a person
        pass

    def post(self,person_id):
        # add new record for a person.
        pass


