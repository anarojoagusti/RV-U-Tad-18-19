from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

#Creo mi lista de usuarios
users = [
    {
    "name": "Ana",
    "age": 23,
    "occupation": "student"
    },
    {
    "name":"Elvin",
    "age": 32,
    "occupation": "Doctor"
    },
    {
    "name": "Jass",
    "age": 22,
    "occupation": "Web Developer"}
]

#Defino la clase users
class User(Resource):
#This REST Api uses standard HTTP response status code
#This method searches for the user in the users_list
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

#This method creates a new user by creating a parser, adding the add_argument
#and occupation arguments, then store them in a variable. If this user does not exist
#yet, we append it to users list
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {"name": name, "age": args["age"], "occupation": args["occupation"]}
        users.append(user)
        return user, 201

#This method checks if the user exists and updates his/her details with the
#parsed arguments
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = rgs["occupation"]
                return user, 200
        user = {"name": name, "age": args["age"], "occupation": args["occupation"]}
        users.append(user)
        return user, 201

#In this method, we specify users_list as a variable in global scope, son when we update
#the user_list using list comprehension to create a list without the mane specified, we return an OK message.
    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 202

api.add_resource(User, "/user/<string:name>")
#<string:name> indicates that it is a variable part in the route which accepts any name
