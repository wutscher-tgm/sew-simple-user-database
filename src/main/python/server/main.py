from flask import Flask
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)


class DB:

    def __init__(self, location):
        self.__db = ""
        self.__location = location
        self.load()

    def get(self):
        return self.__db

    def load(self):
        file = open(self.__location, "r")
        for line in file:
            self.__db += line.rstrip('\n')
        self.__db = json.loads(self.__db)

    def addEntry(self, entry):
        self.__db += entry
        self.save(self.__db)

    def save(self, db):
        file = open(self.__location, "w")
        file.write(json.dumps(db))

class Schueler(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        #parser.add_argument('email', type=str)
        email = parser.parse_args().email
        username = parser.parse_args().username
        #email = parser.parse_args().email
        if(email == None or username == None):
            return "arguments invalid"
        db = DB("db.json")
        db.addEntry([{"email":email,"username":username}])

        return db.get()

api.add_resource(Schueler, '/students')

if __name__ == '__main__':
    app.run(debug=True)