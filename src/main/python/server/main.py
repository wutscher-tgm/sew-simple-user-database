import base64

import werkzeug
from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
true = True
false = False
null = None


app = Flask(__name__)
api = Api(app)


class DB:

    def __init__(self, location):
        self.__db = ''
        self.__location = location
        self.load()

    def get(self, email=null, username=null):
        if email != null:
            for element in self.__db:
                if element['email'] == email:
                    return element
        elif username != null:
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

        if self.__db == '':
            self.__db = '[]'
        self.__db = json.loads(self.__db)

    def addEntry(self, entry):
        if self.get(email=entry[0]['email']) != null:
            return "email already exists"
        self.__db += entry
        self.save(self.__db)
        return "successful"

    def save(self, db):
        file = open(self.__location, "w")
        file.write(json.dumps(db))

class Schueler(Resource):

    def __init__(self):
        self.__db = DB("db.json")


    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='args')
        parser.add_argument('username', type=str, location='args')
        parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
        picture = parser.parse_args().picture
        username = parser.parse_args().username
        email = parser.parse_args().email
        picture = base64.b64encode(picture.read())
        
        if(email == null or username == null):
            return "arguments invalid"
        return self.__db.addEntry(
            [
                {"email": email,
                 "username": username,
                 "picture": picture.decode("utf-8")
                 }
            ]
        )

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        email = parser.parse_args().email
        username = parser.parse_args().username

        if email != null:
            return self.__db.get(email=email)
        elif username != null:
            return self.__db.get(username=username)
        else:
            return self.__db.get()

    def patch(self):
        pass

    def delete(self):
        pass

api.add_resource(Schueler, '/students')

if __name__ == '__main__':
    app.run(debug=true)