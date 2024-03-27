from flask_restful import Resource, reqparse
from flask import request
from app.models.TimeSlot import TimeSlot
from flask import abort


class TimeSlots(Resource):

    def post(self, username):
        data = request.get_json()

        # Ensure data is a list
        if not isinstance(data, list):
            return {'message': 'Invalid data format. Expected a list.'}, 400

        for item in data:
            parser = reqparse.RequestParser()

            parser.add_argument('day_name', type=str, required=True)
            parser.add_argument('start_time', type=str, required=True)
            parser.add_argument('end_time', type=str, required=True)

            args = item

            try:
                timeslot = TimeSlot()
                timeslot.createTimeSlot(username, **args)
                return {'message': 'Time slot created successfully',
                    'data': args}
            except Exception as e:
                return {'message': f'Error creating patient: {str(e)}'}, 500

    def get(self, username):
        day_name = request.args.get("day_name")
        if day_name:
            try:
               slots = TimeSlot.get_time_slots_by_doctor_username_day(username, day_name)
               if slots:
                   return {"data": slots}
               else:
                   return {"message": "Time slots not found for this doctor"}, 404
            except Exception as e:
                abort(500, "Internal Server Error")

        else:
            try:
                slots = TimeSlot.get_time_slots_by_doctor_username(username)
                if slots:
                    return {"data": slots}
                else:
                    return {"message": "Time slots not found for this doctor"}, 404
            except Exception as e:
                abort(500, "Internal Server Error")

    def put(self, username):
        data = request.get_json()

        # Ensure data is a list
        if not isinstance(data, list):
            return {'message': 'Invalid data format. Expected a list.'}, 400

        try:
            timeslots = TimeSlot.get_time_slots_by_doctor_username(username)
            if timeslots:
                TimeSlot.delete_time_slots(timeslots)
            else:
                return {"message": "There is no existing record"}, 404
        except Exception as e:
            return {'message': f'Error in finding existing record: {str(e)}'}, 500

        for item in data:
            parser = reqparse.RequestParser()

            parser.add_argument('day_name', type=str, required=True)
            parser.add_argument('start_time', type=str, required=True)
            parser.add_argument('end_time', type=str, required=True)

            args = item
            try:
                timeslot = TimeSlot()
                timeslot.createTimeSlot(username, **args)
            except Exception as e:
                return {'message': f'Error while updating: {str(e)}'}, 500

    def delete(self, username):
        isAll = request.args.get("is_all")
        try:
            if isAll.lower().__eq__("true"):
                TimeSlot.delete_all_time_slots()
                return {"message": "Deleted all records"}
            else:
                timeslots = TimeSlot.get_time_slots_by_doctor_username(username)
                if timeslots:
                    TimeSlot.delete_time_slots(timeslots)
                else:
                    return {"message": "There is no existing record"}, 404
                return {"message": "Deleted all records for username"}
        except Exception as e:
            return {'message': f'Error deleting Time Slot: {str(e)}'}, 500