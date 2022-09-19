from flask import Flask
from flask_restx import Api, Resource
from models import UserPayload
from listed.persistence import db

# CONFIGURATION of the APPs
app = Flask(__name__)
api = Api(app, version="1.0", title="Social Media API", description="APIs to Make Connections")
ns = api.namespace('')
#global variables
db_access = db.SocialStorage()


@ns.route("/create")
class CreateUser(Resource):
    api.models[UserPayload.name] = UserPayload
    @ns.expect(UserPayload)
    def post(self):
        user_data = api.payload
        res = db_access.createUsers(user_data['username'])
        if res == 400:
            return {
                'status': 'failure',
                'reason': 'User Already Exists'
            }, 400
        else:
            return {
                'status': 'success'
            }, 201

@ns.route("/add/<userA>/<userB>")
class ConnectUser(Resource):
    def post(self, userA, userB):
        res = db_access.connectFriends(userA, userB)
        if res == 400:
            return {
                'status': 'failure',
                'reason': 'Users already friends'
            }, 400
        elif res == 404:
            return {
                       'status': 'failure',
                       'reason': 'Users do not exist'
                   }, 400
        else:
            return {
                'status': 'success'
            }, 202

@ns.route("/friends/<userA>")
class GetFriends(Resource):
    def get(self, userA):
        res = db_access.getFriends(userA)
        if res == 400:
            return {
                'status': 'failure',
                'reason': 'User does not exist'
            }, 400
        elif res == 404:
            return {
                       'status': 'failure',
                       'reason': 'User has no friends'
                   }, 404
        else:
            return {
                'friends': res
            }, 203



if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=8080)