from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import abort

from app.models.patient import Patient


class PatientResource(Resource):

    # @jwt_required()
    def get(self, username):
        try:
            patient = Patient.get_patient_by_username(username)
            return {'data': patient}
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        try:
            new_patient = Patient()
            new_patient.create_patient(**args)
            return {'message': 'Patient created successfully',
                    'data': new_patient.get_patient_by_username(args['username'])}
        except Exception as e:
            return {'message': f'Error creating patient: {str(e)}'}, 500

    # @jwt_required()
    def put(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('contact_number', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('DOB', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        args = parser.parse_args()
        try:
            patient = Patient.get_patient_by_username(username)
            if patient is not None:
                response = Patient.update_patient(username, **args)
                return {'message': 'Patient updated successfully', 'data': response}
            else:
                abort(404, message="Patient not found")
        except Exception as e:
            return {'message': f'Error updating patient: {str(e)}'}, 500

    # @jwt_required()
    def delete(self, patient_id):
        try:
            patient = Patient.get_patient_by_username(patient_id)
            if patient:
                patient.delete_patient()
                return {'message': 'Patient deleted successfully'}
            else:
                abort(404, message="Patient not found")
        except Exception as e:
            return {'message': f'Error deleting patient: {str(e)}'}, 500
