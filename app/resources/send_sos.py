# Initialize the SNS client
import os

import boto3
from flask_restful import Resource
from twilio.rest import Client

from app.models import Patient

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = '+15067045241'
client = Client(account_sid, auth_token)
hospital_number = '+14376610738'


class SendSOS(Resource):
    def post(self, username):
        # Retrieve the phone number associated with the username (you need to implement this)
        patient = Patient.get_patient_by_username(username)
        if patient is None:
            return {'message': 'Unable to find the Patient'}, 404

        # Send the SOS message
        message = ('Send Help to ' + patient['name'] + ' contact number +' + patient['contact_number'] + ' address ' +
                   patient['address'])
        response = client.messages.create(
         body=message,
         from_=twilio_number,
         to=hospital_number
     )
        return {'message': 'SOS message sent successfully'}, 200
