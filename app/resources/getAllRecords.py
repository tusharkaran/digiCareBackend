from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import abort

from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.record import RecordedData

class PatientAllResources(Resource):

    # @jwt_required()
    def get(self):
        try:
            patient = Patient.get_all_patients()
            return {'data': patient}
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))


class DoctorAllResources(Resource):

    # @jwt_required()
    def get(self):
        try:
            patient = Doctor.get_all_doctors()
            return {'data': patient}
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))


class AllRecordedDataResource(Resource):
    def get(self):
        try:
            record = RecordedData.get_all_records()
            return {'data': record}
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))