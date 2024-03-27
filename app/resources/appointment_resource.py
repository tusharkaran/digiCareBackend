from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import abort, request

from app.models.appointment import Appointment


class AppointmentResource(Resource):

    def post(self, username):

        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('doctor_username', type=str, required=True)
        parser.add_argument('day', type=str, required=True)
        parser.add_argument('time', type=str, required=True)
        parser.add_argument('description', type=str, required=True)

        args = parser.parse_args()

        try:
            new_appointment = Appointment()
            new_appointment.create_appointment(username,**args)
            return {'message': 'Appointment created successfully'}
                  #  'data': new_appointment.get_patient_by_username(args['username'])}
        except Exception as e:
            return {'message': f'Error creating patient: {str(e)}'}, 500

    def get(self, username):
        isAll = request.args.get("is_all")
        try:
            if isAll.lower().__eq__("true"):
                appointments = Appointment.get_all_appointments()
                if appointments:
                    return appointments
                else:
                    return {"message": "Appointments are empty"}, 404
            else:
                appointments = Appointment.get_appointments_by_patient_username(username)
                if appointments:
                    return appointments
                else:
                    return {"message": "Appointments not found for this patient"}, 404
        except Exception as e:
            abort(500, "Internal Server Error")

    def delete(self, username):
        try:
            appointments = Appointment.get_appointments_by_patient_username(username)
            if appointments:
                Appointment.delete_appointments(appointments)
                return {"message": "Deleted All Appointments for username"}
            else:
                return {"message": "No appointment were found for patient - " + username}, 404
        except Exception as e:
            abort(500, message=str(e))

