import base64
import urllib
import os
import hashlib

import werkzeug
from flask import Flask
import flask
from flask_restful import Resource, Api, reqparse
import json
from flask_httpauth import HTTPBasicAuth
from argon2 import PasswordHasher
from flask_cors import CORS
from flask import request, session

true = True
false = False
null = None


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
                    element2 = {
                        "email": element['email'],
                        "username": element['username'],
                        "picture": element['picture'],
                        "isAdmin": element['isAdmin']
                    }
                    return element2
        else:
            return self.__db
    
    def getUser(self, email):
        if email != null:
            for element in self.__db:
                if element['email'] == email:
                    return element
        else:
            return null
    

    def update(self, email, username=null, picture=null, password=null):
        if email != null:
            for element in self.__db:
                if element['email'] == email:
                    if username != null:
                        element['username'] = username
                    if picture != null:
                        element['picture'] = picture
                    if password != null:
                        element['password'] = password
                    self.save(self.__db)
                    return 1
            return None

    def isAdmin(self, email):
        for element in self.__db:
                if element['email'] == email:
                    return element['isAdmin']

    def delete(self, email):
        entry = self.get(email=email)
        if entry == None:
            return None
        self.__db.remove(entry)
        self.save(self.__db)

app = Flask('SimpleUserDatabase')
api = Api(app)
ph = PasswordHasher()

CORS(app, resources={r"/*": {"origins": "*"}})

auth = HTTPBasicAuth()
db = DB("db.json")

db.addEntry([{
    "email": "admin@userdb.com", 
    "username": "admin",
    "picture": null,
    "password": ph.hash("admin"),
    "isAdmin": True
}])

@auth.verify_password
def verify_pw(username, password):
    print(username)
    print(password)
    app.logger.info('Userneme: %s', username)
    app.logger.info('Password: %s', password)
    user = db.getUser(username)
    stored_pw = null
    app.logger.info('User: %s', user)
    if user != None:
        stored_pw = user['password']
    else:
        return False
    return ph.verify(stored_pw, password)

from functools import wraps
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not db.isAdmin(auth.username()):
            return "only for administrators", 502
        else:
            return f(*args, **kwargs)
    return decorated

class Schueler(Resource):

    def __init__(self):
        pass
    
    @auth.login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        email = parser.parse_args().email

        if email != null:
            data = db.get(email=email)
            if(data == None): return "user not found", 404
            return data, 200
        else:
            return db.get()
    
    @auth.login_required
    @admin_required
    def post(self):
        # Getting arguments from request
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('pictureLink', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('isAdmin')

        # Loading arguments into easily usable variables
        pictureB64 = parser.parse_args().picture
        pictureLink = parser.parse_args().pictureLink
        username = parser.parse_args().username
        email = parser.parse_args().email
        picture = null
        isAdmin = parser.parse_args().isAdmin
        
        password = None
        if(parser.parse_args().password != None):
            password = ph.hash(parser.parse_args().password)

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

        if isAdmin == None:
            isAdmin = False
        if isAdmin.lower() == "true":
            isAdmin = True
        else:
            isAdmin = False
        
        return db.addEntry(
            [
                {"email": email,
                 "username": username,
                 "picture": picture,
                 "password": password,
                 "isAdmin": isAdmin
                 }
            ]
        )

    @auth.login_required
    @admin_required
    def patch(self):
        # Getting arguments from request
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('pictureLink', type=str)
        parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')

        # Loading arguments into easily usable variables
        pictureB64 = parser.parse_args().picture
        pictureLink = parser.parse_args().pictureLink
        username = parser.parse_args().username
        email = parser.parse_args().email
        password = parser.parse_args().password
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

        result = db.update(email, username=username, picture=picture, password=ph.hash(password))
        if result == None:
            return "user not found", 404
        return result

    @auth.login_required
    @admin_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        email = parser.parse_args().email
        result = db.delete(email)
        if result == None:
            return "user not found", 404


api.add_resource(Schueler, '/')


if __name__ == '__main__':
    app.run(debug=true, host='0.0.0.0', port=80)