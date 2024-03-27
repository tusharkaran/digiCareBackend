from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import abort, request

from app.models.doctor import Doctor


class DoctorResource(Resource):
    # @jwt_required()
    def get(self, username):
        try:
            # parser = reqparse.RequestParser()
            # parser.add_argument('username', type=str, required=True)
            # args = parser.parse_args()
            doctor = Doctor.get_doctor_by_username(username)
            return {'data': doctor}
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('specialization', type=str, required=True)
        parser.add_argument('contact_info', type=dict, required=True)
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        try:
            new_doctor = Doctor()
            response = new_doctor.create_doctor(**args)
            return {'message': 'Doctor created successfully', 'data': response}
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def put(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('specialization', type=list, required=False)
        parser.add_argument('address', type=str, required=False)
        parser.add_argument('study_history', type=list, required=False)
        parser.add_argument('contact_number', type=str, required=False)
        parser.add_argument('availability_hours', type=list, required=False)
        parser.add_argument('Hospital', type=str, required=False)
        args = request.get_json()

        try:
            doctor = Doctor.get_doctor_by_username(username)
            if doctor is not None:
                response = Doctor.update_doctor(username,**args)
                return {'message': 'Doctor updated successfully', 'data': response}
            else:
                abort(404, message="Doctor not found")
        except Exception as e:
            abort(500)

    # @jwt_required()
    def delete(self, username):

        try:
            doctor = Doctor.get_doctor_by_username(username)
            if doctor:
                response = doctor.delete_doctor()
                return {'message': 'Doctor deleted successfully', 'data': response}
            else:
                abort(404, message="Doctor not found")
        except Exception as e:
            abort(500, message=str(e))
