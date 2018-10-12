from flask import Flask
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)



class Schueler(Resource):
    def load_db(self, location):
        file = open(location, "r")
        database = ""
        for line in file:
            database += line.rstrip('\n')
        return json.loads(database)

    def save_db(self, db, location):
        file = open(location, "w")
        file.write(json.dumps(db))

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
        database = self.load_db("db.json")
        database += [{"email":email,"username":username}]
        self.save_db(database, "db.json")

        return database
api.add_resource(Schueler, '/students')

if __name__ == '__main__':
    app.run(debug=True)