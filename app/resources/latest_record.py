from flask_restful import Resource, reqparse
from flask import abort
from app.models.record import RecordedData
from uuid import uuid4


class LatestRecord(Resource):

    def get(self, username):
        try:
            record = RecordedData.get_latest_record(username)
            if record:
                return {'data': record}
            else:
                return {'message': "Record not found"}

        except Exception as e:
            abort(500)
