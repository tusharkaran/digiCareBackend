from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.patient import Patient
from app.utils.auth import verify_password


class PatientLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        patient = Patient.get_patient_by_username(args['user_name'])
        if patient and verify_password(args['password'], patient['password']):
            access_token = create_access_token(identity=args['user_name'])
            refresh_token = create_refresh_token(identity=args['user_name'])
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        else:
            return {'message': 'Invalid username or password'}, 401
