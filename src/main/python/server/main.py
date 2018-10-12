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

    def get(self, email=None, username=None):
        if email != None:
            for element in self.__db:
                if element['email'] == email:
                    return element
        elif username != None:
            rs = []
            for element in self.__db:
                if element['username'] == username:
                    rs += [element]
            return rs
        else:
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

    def __init__(self):
        self.__db = DB("db.json")


    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        #parser.add_argument('email', type=str)
        email = parser.parse_args().email
        username = parser.parse_args().username
        #email = parser.parse_args().email
        if(email == None or username == None):
            return "arguments invalid"
        self.__db.addEntry([{"email": email, "username": username}])
        return 1

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        email = parser.parse_args().email
        username = parser.parse_args().username

        if email != None:
            return self.__db.get(email=email)
        elif username != None:
            return self.__db.get(username=username)
        else:
            return self.__db.get()

    def patch(self):
        pass

    def delete(self):
        pass

api.add_resource(Schueler, '/students')

if __name__ == '__main__':
    app.run(debug=True)