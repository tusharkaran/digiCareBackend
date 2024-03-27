# from flask_restful import Resource, reqparse, abort
# from app.utils.auth import create_token, verify_password
#
#
# class AuthResource(Resource):
#     def post(self):
#         try:
#             parser = reqparse.RequestParser()
#             parser.add_argument('username', help='This field cannot be blank', required=True)
#             parser.add_argument('password', help='This field cannot be blank', required=True)
#             args = parser.parse_args()
#
#             username = args['username']
#             password = args['password']
#
#             user_type = 'patient'  # Assuming patient by default, can be changed based on your requirements
#             if verify_password(user_type, username, password):
#                 access_token = create_token(username)
#                 return {'access_token': access_token}, 200
#             else:
#                 abort(401, message="Invalid credentials")  # Unauthorized if authentication fails
#         except Exception as e:
#             abort(500, message=f"Authentication error: {str(e)}")
