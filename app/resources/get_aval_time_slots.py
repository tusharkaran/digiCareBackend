from flask_restful import Resource, reqparse, abort
from flask import request

from app.models import TimeSlot
from app.models.appointment import Appointment


class GetAvailTimeSlot(Resource):
    def get(self, doctor_username):
        day_name = request.args.get("day_name")
        try:
            time_slot = TimeSlot()
            if day_name:
                slots = TimeSlot.get_time_slots_by_doctor_username_day(doctor_username, day_name)
            else:
                slots = time_slot.get_time_slots_by_doctor_username(doctor_username)
            booked_appointments = Appointment.query_appointments(doctor_username)
            # Iterate over slots and appointments
            if booked_appointments:
                for slot in slots:
                    for appointment in booked_appointments:
                        if (slot['day_name'] == appointment['day'] and
                                slot['start_time'] == appointment['time'] and
                                slot['doctor_username'] == appointment['doctor_username']):
                            slot['is_booked'] = True
                            break
            return slots
        except Exception as e:
            abort(500)
