from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
#from app.models.patient import Patient
from app.models.admin import Admin
from app.utils.auth import verify_password


class AdminLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        admin = Admin.get_admin_by_username(args['user_name'])
        if admin and verify_password(args['password'], admin['password']):
            access_token = create_access_token(identity=args['user_name'])
            refresh_token = create_refresh_token(identity=args['user_name'])
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        else:
            return {'message': 'Invalid username or password'}, 401
