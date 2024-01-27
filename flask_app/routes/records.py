from flask_restx import Resource, Namespace, fields
from flask_app import db
from flask_app.models.Record import Record
from flask import request
from flask_app.models.User import User

records_ns = Namespace('records', description='Record related operations')

record_get_model = records_ns.model('Record', {
    'id': fields.Integer(description='The record ID in the database'),
    'user_id': fields.String(description='The firebase UID of the currently logged in user'),
    'text': fields.String(description='The text to be recorded'),
    'created_at': fields.String(description='The time the record was made')
})

record_post_model = records_ns.model('Record', {
    'text': fields.String(description='The text to be recorded')
})

@records_ns.route('/')
class RecordsList(Resource):
    @records_ns.marshal_with(record_get_model)
    def get(self):
        records = Record.query.all()
        return records

@records_ns.route('/<string:firebase_uid>')
@records_ns.response(404, 'User not found')
class UserRecordResource(Resource):
    @records_ns.marshal_with(record_get_model)
    def get(self, firebase_uid):
        user = User.query.filter_by(firebase_uid=firebase_uid).first_or_404()
        records = Record.query.filter_by(user_id=user.id).all()
        return records
    
    @records_ns.expect(record_post_model)
    def post(self, firebase_uid):
        data = request.json
        user = User.query.filter_by(firebase_uid=firebase_uid).first_or_404()
        data["user_id"] = user.id
        record = Record.create_record(data)
        return {'message': 'Record created successfully.', 'record': record.id}, 201

@records_ns.route('/<int:record_id>')
@records_ns.response(404, 'Record not found')
class RecordResource(Resource):
    @records_ns.marshal_with(record_get_model)
    def get(self, record_id):
        record = Record.query.filter_by(id=record_id).first_or_404()
        return record
    
    @records_ns.expect(record_post_model)
    def put(self, record_id):
        data = request.json
        record = Record.query.filter_by(id=record_id).first_or_404()
        Record.update_record(record, data)
        return {'message': 'Record updated successfully.', 'record_id': record.id}, 200
