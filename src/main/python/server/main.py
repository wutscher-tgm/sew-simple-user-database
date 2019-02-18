
import base64
import urllib
import os

import werkzeug
import authdigest
from flask import Flask
import flask
from flask_restful import Resource, Api, reqparse
import json
from argon2 import PasswordHasher
ph = PasswordHasher()

true = True
false = False
null = None

app = Flask('SimpleUserDatabase')
api = Api(app)

from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}})

tokens = []

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
    
    def getUser(self, email=null):
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

    def delete(self, email):
        entry = self.get(email=email)
        if entry == None:
            return None
        self.__db.remove(entry)
        self.save(self.__db)

# AUTH
from functools import wraps

class FlaskRealmDigestDB():#(authdigest.RealmDigestDB):
    def __init__(self, db):
        self.db = db

    def requires_auth(self, f):
        """@wraps(f)
        def decorated(*args, **kwargs):
            request = flask.request
            print("Authenticated:  " + str(self.isAuthenticated(request).authenticated))
            if not self.isAuthenticated(request).authenticated:
                return self.challenge()
            #print('Wrapping now')
            return f(*args, **kwargs)
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            if app.testing:
                return f(*args, **kwargs)
            if 'tok' in flask.request.cookies:
                token = flask.request.cookies['tok']
                for element in tokens:
                    if element['token'] == token:
                        return f(*args, **kwargs)
                return 'user not found'
            else:
                print('no cookie')
                return 'no cookie'

        return decorated
# AUTH
import random
import string

from flask import request, session  
class Schueler(Resource):

    authDB = FlaskRealmDigestDB(0)
    #('MyAuthRealm', DB("db.json"), algorithm="sha256")
    #authDB.add_user('admin'.encode('utf-8'), 'test'.encode('utf-8'))
    def __init__(self):
        self.__db = DB("db.json")
        #authDB = FlaskRealmDigestDB(self.__db)
    
    @authDB.requires_auth
    def get(self):
        #print(request.authorization.username)
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
    
    def post(self):
        
        # Getting arguments from request
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('pictureLink', type=str)
        parser.add_argument('password', type=str)
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
            return 'argument "email" is missing'
        elif username == null:
            return 'argument "username" is missing'
        elif (pictureB64 != null) and (pictureLink != null):
            return 'too many arguments provided, can only use one picture source'

        if pictureB64 != null:
            picture = (base64.b64encode(pictureB64.read())).decode("utf-8")
        elif pictureLink != null:
            picture = (base64.b64encode((urllib.request.urlopen(pictureLink)).read())).decode("utf-8")

        return self.__db.addEntry(
            [
                {"email": email,
                 "username": username,
                 "picture": picture,
                 "password": ph.hash(password)
                 }
            ]
        )

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

        result = self.__db.update(email, username=username, picture=picture, password=ph.hash(password))
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

    def options(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        email = parser.parse_args().email
        password = parser.parse_args().password

        user = self.__db.getUser(email)

        if user != None:
            try:
                if ph.verify(user['password'], password):
                    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
                    #TODO: check that token doesn't exist
                    tokens.append({
                        'token': token,
                        'user': user['password']
                    })
                    return 'success', {'Set-Cookie': 'tok='+token}
                else:
                    return 'not valid'
            except:
                return 'not valid'
        else:
            return 'not valid'


api.add_resource(Schueler, '/students')


if __name__ == '__main__':
    app.run(debug=true, host='0.0.0.0')