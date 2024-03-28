import decimal, uuid
import logging
import os
from datetime import datetime, timedelta

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import TypeDeserializer
from flask_restful import abort

from app.models.patient import Patient

aws_region = os.getenv('AWS_DEFAULT_REGION')

dynamodb = boto3.resource('dynamodb', region_name=aws_region)
global_table = dynamodb.Table('appointment')


class Appointment:
    def __init__(self):
        self.table = global_table
        self.deserializer = TypeDeserializer()

    @classmethod
    def create_appointment(cls, username,date,doctor_username, day, time, description):

        patient_record = Patient.get_patient_by_username(username)
        if not patient_record:
         return {'message': 'Patient not found'}

        # Extract room_id from patient record
       # room_id = patient_record.get('room_id')
        appointment_instance = cls()
        appointment_instance.bookTimeSlot(doctor_username,time,day)
        room_id = Patient.get_room_id_by_username(username)
        item = {
            "id": str(uuid.uuid4()),
            "patient_username": username,
            "doctor_username": doctor_username,
            "date": date,
            "day": day,
            "time": time,
            "description": description,
            "room_id": room_id
        }
        response = global_table.put_item(Item=item)
        return response

    @classmethod
    def get_all_appointments(cls):
        response = global_table.scan()
        items = response.get('Items', [])
        appointments = [cls.deserialize(item) for item in items]
        return appointments

    @classmethod
    def get_appointments_by_patient_username(cls, patient_username):
        response = global_table.scan(
            FilterExpression='patient_username = :val',
            ExpressionAttributeValues={
                ':val': patient_username
            }
        )
        items = response.get('Items', [])
        appointments = [cls.deserialize(item) for item in items]
        return appointments

    @classmethod
    def get_appointments_by_doctor_username(cls, doctor_username):
        try:
            response = global_table.scan(
                FilterExpression='doctor_username = :val',
                ExpressionAttributeValues={
                    ':val': doctor_username
                }
            )
            items = response.get('Items', [])
            appointments = [cls.deserialize(item) for item in items]
            return appointments
        except Exception as e:
            print(f"An error occurred while fetching appointments: {str(e)}")
            abort(500)

    @classmethod
    def delete_appointments(cls, appointments):
        for item in appointments:
            key = {k['AttributeName']: item[k['AttributeName']] for k in global_table.key_schema}
            print("Deleting item with key:", key)  # Debugging
            global_table.delete_item(Key=key)

        return [cls().deserialize(item) for item in appointments]

    @classmethod
    def deserialize(cls, item):
        if isinstance(item, dict):
            return {key: cls.deserialize(value) for key, value in item.items()}
        elif isinstance(item, list):
            return [cls.deserialize(value) for value in item]
        elif isinstance(item, decimal.Decimal):
            return float(item)  # Convert Decimal to float
        else:
            return item

    def bookTimeSlot(self, doctor_username, start_time, day):
        # Query the table to find the item with matching attributes
        response = global_table.scan(
            FilterExpression='day_name = :day AND doctor_username = :doctor_username AND start_time = :start_time',
          #  ExpressionAttributeNames={'#d': 'day'},  # Use ExpressionAttributeNames to handle reserved keyword
            ExpressionAttributeValues={
                ':doctor_username': doctor_username,
                ':start_time': start_time,
                ':day': day
            }
        )
        items = response.get('Items', [])

        if not items:
            return {'message': 'Appointment not found'}

        # Assuming there's only one matching item, retrieve its primary key
        appointment_id = items[0]['id']

        # Update the item using its primary key
        response = global_table.update_item(
            Key={
                'id': appointment_id
            },
            UpdateExpression='SET is_booked = :val',
            ExpressionAttributeValues={
                ':val': True
            },
            ReturnValues='UPDATED_NEW'
        )
        return response

    @classmethod
    def query_appointments(cls, doctor_username):
        try:
            # Get the current date
            current_date = datetime.now().date()

            # Query appointments for the specified doctor_username
            response = global_table.scan(
                FilterExpression='doctor_username = :val AND #date > :current_date',
                ExpressionAttributeNames={'#date': 'date'},
                ExpressionAttributeValues={
                    ':val': doctor_username,
                    ':current_date': current_date.strftime('%Y-%m-%d')
                }
            )
            items = response.get('Items', [])
            appointments = [cls.deserialize(item) for item in items]
            return appointments
        except Exception as e:
            print(f"An error occurred while querying appointments: {str(e)}")
            return []
