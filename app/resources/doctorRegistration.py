from flask_restful import Resource, reqparse
from flask import request
from app.models.doctor import Doctor


class DoctorRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('contact_number', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('role', type=str, required=True)
        parser.add_argument('DOB', type=str, required=True)
        parser.add_argument('gender', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        parser.add_argument('start_year_of_practice', type=str, required=True)
        parser.add_argument('availability_hours', type=list, required=False)
        parser.add_argument('specialization', type=list, required=True)
        parser.add_argument('study_history', type=list, required=True)
        parser.add_argument('patients', type=list, required=False)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('Hospital', type=str, required=True)
        args = request.get_json()

        try:
            new_doctor = Doctor()
            response = new_doctor.create_doctor(**args)
            return {'message': 'Doctor created successfully', 'data': response}, 201
        except Exception as e:
            return {'message': f'Error creating doctor: {str(e)}'}, 500
