from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import abort

from app.models.alert import Alert


class AlertResource(Resource):
    # @jwt_required()
    def get(self, alert_id):
        try:
            alert = Alert.get_alert_by_id(alert_id)
            return {'data': alert}
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patient', type=str, required=True)
        parser.add_argument('doctor', type=str, required=True)
        parser.add_argument('timestamp', type=str, required=True)
        parser.add_argument('severity', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        args = parser.parse_args()

        try:
            new_alert = Alert()
            response = new_alert.create_alert(**args)
            return {'message': 'Alert created successfully', 'data': response}
        except Exception as e:
            abort(500)

    # @jwt_required()
    def put(self, alert_id):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_id', type=str, required=True)
        parser.add_argument('doctor_id', type=str, required=True)
        args = parser.parse_args()

        try:
            alert = Alert.get_alert_by_id(alert_id)
            if alert:
                response = alert.update_alert(**args)
                return {'message': 'Alert updated successfully', 'data': response}
            else:
                abort(404, message="Alert not found")
        except Exception as e:
            abort(500, message=str(e))

    # @jwt_required()
    def delete(self, alert_id):
        try:
            alert = Alert.get_alert_by_id(alert_id)
            if alert:
                response = alert.delete_alert()
                return {'message': 'Alert deleted successfully', 'data': response}
            else:
                abort(404, message="Alert not found")
        except Exception as e:
            abort(500, message=str(e))
