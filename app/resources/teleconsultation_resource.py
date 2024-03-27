from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import abort

from app.models.teleconsultation import Teleconsultation


class TeleconsultationResource(Resource):
    # @jwt_required()
    def get(self, teleconsultation_id):
        try:
            teleconsultation = Teleconsultation.get_teleconsultation_by_id(teleconsultation_id)
            return {'data': teleconsultation}
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_id', type=str, required=True)
        parser.add_argument('doctor_id', type=str, required=True)
        parser.add_argument('platform', type=str, choices=['Teams', 'Zoom', 'Google Meet'])
        parser.add_argument('scheduled_time', type=str, required=True)
        args = parser.parse_args()

        try:
            new_teleconsultation = Teleconsultation()
            response = new_teleconsultation.create_teleconsultation(**args)
            return {'message': 'Teleconsultation created successfully', 'data': response}
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def put(self, teleconsultation_id):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_id', type=str, required=True)
        parser.add_argument('doctor_id', type=str, required=True)
        parser.add_argument('platform', type=str, choices=['Teams', 'Zoom', 'Google Meet'])
        parser.add_argument('scheduled_time', type=str, required=True)
        args = parser.parse_args()

        try:
            teleconsultation = Teleconsultation.get_teleconsultation_by_id(teleconsultation_id)
            if teleconsultation:
                response = teleconsultation.update_teleconsultation(**args)
                return {'message': 'Teleconsultation updated successfully', 'data': response}
            else:
                abort(404, message="Teleconsultation not found")
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def delete(self, teleconsultation_id):
        try:
            teleconsultation = Teleconsultation.get_teleconsultation_by_id(teleconsultation_id)
            if teleconsultation:
                response = teleconsultation.delete_teleconsultation()
                return {'message': 'Teleconsultation deleted successfully', 'data': response}
            else:
                abort(404, message="Teleconsultation not found")
        except Exception as e:
            abort(500, message=str(e))
