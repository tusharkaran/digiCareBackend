from flask_restful import Resource, reqparse
from flask import abort, request
from app.models.record import RecordedData
from uuid import uuid4
from simulation import HealthRecorder
import tkinter as tk


class RecordedDataResource(Resource):

    def get(self,username):
        try:
            record = RecordedData.get_records_by_patient_username(patient_username=username)
            if record:
                return {'data': record}
            else:
                abort(404, message="Record not found")
        except Exception as e:
            abort(500)

    def post(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_username', type=str, required=True)
        parser.add_argument('timestamp', type=str, required=True)
        parser.add_argument('blood_pressure', type=str, required=True)
        parser.add_argument('heart_rate', type=str, required=True)
        parser.add_argument('o2', type=str, required=True)
        parser.add_argument('temperature', type=str, required=True)
        args = request.get_json()

        try:
            record_id = str(uuid4())
            new_record = RecordedData()
            response = new_record.create_record(record_id, **args)
            # return {'message': 'Record created successfully', 'data': response}
        except Exception as e:
            abort(500, message=str(e))

    def put(self, record_id):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_username', type=str, required=True)
        parser.add_argument('timestamp', type=str, required=True)
        parser.add_argument('bloodpressure', type=str, required=True)
        parser.add_argument('heart_rate', type=str, required=True)
        parser.add_argument('o2', type=str, required=True)
        parser.add_argument('sugar_level', type=str, required=True)
        args = parser.parse_args()

        try:
            old_record = RecordedData()
            record = old_record.get_record_by_id(record_id)
            if record:
                response = record.update_record(record_id, **args)
                return {'message': 'Record updated successfully', 'data': response}
            else:
                abort(404, message="Record not found")
        except Exception as e:
            abort(500, message=str(e))

    def delete(self, record_id):
        try:
            record = RecordedData.get_record_by_id(record_id)
            if record:
                response = record.delete_record(record_id)
                return {'message': 'Record deleted successfully', 'data': response}
            else:
                abort(404, message="Record not found")
        except Exception as e:
            abort(500, message=str(e))


