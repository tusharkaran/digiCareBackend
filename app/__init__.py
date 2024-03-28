from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from dotenv import load_dotenv
import os
from flask_restful_swagger_2 import Api as SwaggerApi
import boto3
from app.resources import PatientRegistration, PatientLogin, DoctorRegistration, DoctorLogin, GetAvailTimeSlot, SendSOS
from flask_cors import CORS
# Load environment variables from .env file
load_dotenv()

# Configure Flask application
app = Flask(__name__)
CORS(app)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "supports_credentials": True,
            "Access-Control-Allow-Credentials": True,
        }
    },
)
# Configure JWT secret key
app.config['JWT_SECRET_KEY'] = '123456789'  # Change this to a random secret key
jwt = JWTManager(app)

# Configure Flask-RESTful API
api = Api(app)
# Configure AWS credentials and region
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')

# Configure Boto3 client for DynamoDB
dynamodb = boto3.resource("dynamodb",
                          region_name=aws_region,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)


# Define a resource to check DynamoDB connection
class DynamoDBConnection(Resource):
    def get(self):
        try:
            # Attempt to list DynamoDB tables
            table_list = list(dynamodb.tables.all())
            return {"message": "DynamoDB connection successful", "tables": [table.name for table in table_list]}, 200
        except Exception as e:
            # If an exception occurs, return an error message
            return {"error": str(e)}, 500


# Import and add resources to the API
from app.resources.patient_resource import PatientResource
from app.resources.doctor_resource import DoctorResource
from app.resources.alert_resource import AlertResource
from app.resources.teleconsultation_resource import TeleconsultationResource
from app.resources.health_record_resource import HealthRecordResource
from app.resources.DoctorPatient import DoctorPatientResource
from app.resources.getAllRecords import PatientAllResources, DoctorAllResources, AllRecordedDataResource
from app.resources.recorded_data import RecordedDataResource
from app.resources.latest_record import LatestRecord
from app.resources.timeSlots_resource import TimeSlots
from app.resources.appointment_resource import AppointmentResource
from app.resources.appointment_doctor_resource import AppointmentDoctorResource
from app.resources.adminLogin import AdminLogin

api.add_resource(PatientAllResources, '/api/patient')
api.add_resource(DoctorAllResources, '/api/doctors')
api.add_resource(AllRecordedDataResource, '/api/all-record-data')
api.add_resource(PatientResource, '/api/patient/<username>')
api.add_resource(DoctorResource, '/api/doctor/<username>')
api.add_resource(AlertResource, '/api/alert')
api.add_resource(TeleconsultationResource, '/api/teleconsultation')
api.add_resource(HealthRecordResource, '/api/health-record/<username>')
# api.add_resource(HealthRecordResource, '/api/health-record/latest/<username>')
api.add_resource(PatientRegistration, '/api/register-patient')
api.add_resource(PatientLogin, '/api/patient-login')
api.add_resource(DoctorRegistration, '/api/register-doctor')
api.add_resource(DoctorLogin, '/api/doctor-login')
api.add_resource(DynamoDBConnection, '/check_dynamodb_connection')
api.add_resource(DoctorPatientResource, '/api/doctorpatientrelation')
api.add_resource(RecordedDataResource, '/api/record-data/<username>')
api.add_resource(LatestRecord, '/api/latest-record/<username>')
api.add_resource(TimeSlots, '/api/time-slots/<username>')
api.add_resource(AppointmentResource, '/api/book-appointment/<username>')
api.add_resource(AppointmentDoctorResource, '/api/book-appointment/doctor/<doctor_username>')
api.add_resource(GetAvailTimeSlot,'/api/avail-doc-appointment/<doctor_username>')
api.add_resource(AdminLogin, '/api/admin-login')
api.add_resource(SendSOS, '/api/send-sos/<username>')
swagger = SwaggerApi(app, api_spec_url='/apidocs')

