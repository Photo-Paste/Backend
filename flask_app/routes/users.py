from flask_restx import Resource, Namespace, fields
from flask_app import db
from flask_app.models.User import User
from flask import request

users_ns = Namespace('users', description='User related operations')

user_get_model = users_ns.model('User', {
    'name': fields.String(description='The user name'),
    'firebase_uid': fields.String(description='The firebase_uid'),
    'is_admin': fields.Boolean(description='Indicates if the user is an administrator', required=True),
    'email': fields.String(description='The email of the user'),
    'profile_image_url': fields.String(description='URL of the user\'s profile image'),
    'active': fields.Boolean(description='Indicates if the user account is active')
})

user_post_model = users_ns.model('User', {
    'name': fields.String(description='The user name'),
    'is_admin': fields.Boolean(description='Indicates if the user is an administrator', required=True),
    'email': fields.String(description='The email of the user'),
    'profile_image_url': fields.String(description='URL of the user\'s profile image'),
    'active': fields.Boolean(description='Indicates if the user account is active')
})

@users_ns.route('/')
class UserList(Resource):
    @users_ns.marshal_with(user_get_model)
    def get(self):
        users = User.query.all()
        return users

@users_ns.route('/<string:firebase_uid>')
@users_ns.response(404, 'User not found')
class UserResource(Resource):
    @users_ns.marshal_with(user_get_model)
    def get(self, firebase_uid):
        user = User.query.filter_by(firebase_uid=firebase_uid).first_or_404()
        return user
    
    @users_ns.expect(user_post_model)
    def post(self, firebase_uid):
        data = request.json
        data["firebase_uid"] = firebase_uid
        user = User.create_user(data)
        return {'message': 'User created successfully.', 'user': user.name}, 201

    @users_ns.expect(user_post_model)
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
            users_ns.abort(404, 'User not found')
