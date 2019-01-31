import base64
import urllib
import sys
import os

import werkzeug
from flask import Flask
from flask_restful import Resource, Api, reqparse
import json

true = True
false = False
null = None

app = Flask('SimpleUserDatabase')
api = Api(app)

from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}})


class DB:
    def __init__(self, location):
        self.__db = ''
        self.__location = location
        self.load()

    def load(self):
        if not os.path.isfile(self.__location):
            with open(self.__location, "w+"):
                print("new file created")
        file = open(self.__location, "r+")
        for line in file:
            self.__db += line.rstrip('\n')

        if self.__db == '':
            self.__db = '[]'
        self.__db = json.loads(self.__db)

    def save(self, db):
        file = open(self.__location, "w")
        file.write(json.dumps(db))

    def addEntry(self, entry):
        if self.get(email=entry[0]['email']) != null:
            return "email already exists"
        self.__db += entry
        self.save(self.__db)
        return "successful"

    def get(self, email=null):
        if email != null:
            for element in self.__db:
                if element['email'] == email:
                    return element
        else:
            return self.__db

    def update(self, email, username=null, picture=null):
        if email != null:
            for element in self.__db:
                if element['email'] == email:
                    if username != null:
                        element['username'] = username
                    if picture != null:
                        element['picture'] = picture
                    self.save(self.__db)
                    return 1
            return None

    def delete(self, email):
        entry = self.get(email=email)
        if entry == None:
            return None
        self.__db.remove(entry)
        self.save(self.__db)


class Schueler(Resource):

    def __init__(self):
        self.__db = DB("db.json")

    def post(self):
        # Getting arguments from request
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('pictureLink', type=str)
        parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')

        # Loading arguments into easily usable variables
        pictureB64 = parser.parse_args().picture
        pictureLink = parser.parse_args().pictureLink
        username = parser.parse_args().username
        email = parser.parse_args().email
        picture = null

        # Checking if arguments are valid
        if email == null:
            return 'argument "email" is missing'
        elif username == null:
            return 'argument "username" is missing'
        elif (pictureB64 != null) and (pictureLink != null):
            return 'too many arguments provided, can only use one picture source'

        if pictureB64 != null:
            picture = (base64.b64encode(pictureB64.read())).decode("utf-8")
        elif pictureLink != null:
            picture = (base64.b64encode((urllib.request.urlopen(pictureLink)).read())).decode("utf-8")

        if (email == null or username == null):
            return "arguments invalid"
        return self.__db.addEntry(
            [
                {"email": email,
                 "username": username,
                 "picture": picture
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
            data = self.__db.get(email=email)
            if(data == None): return "user not found", 404
            return data, 200
        else:
            return self.__db.get()

    def patch(self):
        # Getting arguments from request
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('pictureLink', type=str)
        parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')

        # Loading arguments into easily usable variables
        pictureB64 = parser.parse_args().picture
        pictureLink = parser.parse_args().pictureLink
        username = parser.parse_args().username
        email = parser.parse_args().email
        picture = null

        # Checking if arguments are valid
        if email == null:
            return 'argument "email" is missing', 404
        elif (pictureB64 != null) and (pictureLink != null):
            return 'too many arguments provided, can only use one picture source', 500

        if pictureB64 != null:
            picture = (base64.b64encode(pictureB64.read())).decode("utf-8")
        elif pictureLink != null:
            picture = (base64.b64encode((urllib.request.urlopen(pictureLink)).read())).decode("utf-8")

        result = self.__db.update(email, username=username, picture=picture)
        if result == None:
            return "user not found", 404
        return result

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        email = parser.parse_args().email
        result = self.__db.delete(email)
        if result == None:
            return "user not found", 404


api.add_resource(Schueler, '/students')


if __name__ == '__main__':
    app.run(debug=true, host='0.0.0.0')
