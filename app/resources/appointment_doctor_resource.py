from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import abort

from app.models.appointment import Appointment


class AppointmentDoctorResource(Resource):

    def get(self, doctor_username):
        try:
            appointments = Appointment.get_appointments_by_doctor_username(doctor_username)
            if appointments:
                return appointments
            else:
                return {"message": "Appointments not found for this doctor"}, 404
        except Exception as e:
            abort(500, message="Internal Server Error")

    def delete(self, doctor_username):
        try:
            appointments = Appointment.get_appointments_by_doctor_username(doctor_username)
            if appointments:
                Appointment.delete_appointments(appointments)
                return {"message": "Deleted All Appointments for doctor - " + doctor_username}
            else:
                return {"message": "No appointment were found for doctor - " + doctor_username}, 404
        except Exception as e:
            abort(500, message=str(e))
