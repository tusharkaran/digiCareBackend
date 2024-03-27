from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import abort

from app.models.health_record import HealthRecord


class HealthRecordResource(Resource):
    # @jwt_required()
    def get(self, patient_username):
        try:
            health_records = HealthRecord.get_health_record_by_patient(patient_username)
            return {'data': health_records}
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def post(self, patient_username):
        parser = reqparse.RequestParser()
        parser.add_argument('timestamp', type=str, required=True)
        parser.add_argument('records', type=list, required=True)
        args = parser.parse_args()
        args['patient_username'] = patient_username

        try:
            new_health_record = HealthRecord()
            response = new_health_record.create_health_record(**args)
            return {'message': 'Health Record created successfully', 'data': response}
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def put(self, health_record_id):
        parser = reqparse.RequestParser()
        parser.add_argument('records', type=list, required=True)
        args = parser.parse_args()

        try:
            health_record = HealthRecord.get_health_record_by_id(health_record_id)
            if health_record:
                response = health_record.update_health_record(**args)
                return {'message': 'Health Record updated successfully', 'data': response}
            else:
                abort(404, message="Health Record not found")
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def delete(self, health_record_id):
        try:
            health_record = HealthRecord.get_health_record_by_id(health_record_id)
            if health_record:
                response = health_record.delete_health_record()
                return {'message': 'Health Record deleted successfully', 'data': response}
            else:
                abort(404, message="Health Record not found")
        except Exception as e:
            abort(500, message=str(e))

    def get_latest_record_for_patient(self, patient_username):
        try:
            latest_record = HealthRecord.get_latest_health_record(patient_username)
            if latest_record:
                return {'data': latest_record}
            else:
                abort(404, message="No health record found for the patient")
        except Exception as e:
            abort(500, message=str(e))