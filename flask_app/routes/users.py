from flask_restx import Resource, Namespace, fields
from flask_app import db
from flask_app.models.User import User
from flask import request
import uuid

api = Namespace('users', description='User related operations')

# Model for input (POST/PUT requests)
user_model = api.model('User', {
    'name': fields.String(description='The user name'),
    'is_admin': fields.Boolean(description='Indicates if the user is an administrator', required=True),
    'email': fields.String(description='The email of the user'),
    'profile_image_url': fields.String(description='URL of the user\'s profile image'),
    'bio': fields.String(description='The user\'s biography'),
    'active': fields.Boolean(description='Indicates if the user account is active')
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        users = User.query.all()
        return users

@api.route('/<string:firebase_uid>')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, firebase_uid):
        user = User.query.filter_by(firebase_uuid=firebase_uid).first_or_404()
        return user
    
    @api.expect(user_model)
    def post(self, firebase_uid):
        data = request.json
        data["firebase_uid"] = firebase_uid
        user = User.create_user(data)
        return {'message': 'User created successfully.', 'user': user.name}, 201

    @api.expect(user_model)
    def put(self, firebase_uid):
        data = request.json
        user = User.query.filter_by(firebase_uid=firebase_uid).first_or_404()
        User.update_user(user, data)
        return {'message': 'User updated successfully.'}, 200

    def delete(self, firebase_uid):
        result = User.delete_user(firebase_uid)
        if result:
            return {'message': 'User deleted successfully.'}, 200
        else:
            api.abort(404, 'User not found')
