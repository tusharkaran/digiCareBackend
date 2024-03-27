from flask_jwt_extended import create_access_token
from flask_restful import abort
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

bcrypt = Bcrypt()


def verify_password(input_password, password):
    try:
        if password_check(password, input_password):
            return True
        return False
    except Exception as e:
        abort(500, message=f"Error verifying password: {str(e)}")


# def authenticate(user_type):
#     try:
#         parser = reqparse.RequestParser()
#         parser.add_argument('username', help='This field cannot be blank', required=True)
#         parser.add_argument('password', help='This field cannot be blank', required=True)
#         args = parser.parse_args()
#
#         username = args['username']
#         password = args['password']
#
#         if verify_password(user_type, username, password):
#             access_token = create_token(username)
#             return {'access_token': access_token}, 200
#         else:
#             abort(401, message="Invalid credentials")
#     except Exception as e:
#         abort(500, message=f"Authentication error: {str(e)}")

# def identity():
#     try:
#         current_user = get_jwt_identity()
#         return {'user': current_user}
#     except Exception as e:
#         abort(500, message=f"Error identifying user: {str(e)}")

def password_hash(password):
    return generate_password_hash(password)

def password_check(input_password_hash, password):
    return check_password_hash(input_password_hash, password)
