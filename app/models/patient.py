import decimal
import os
from uuid import uuid4

import boto3
from boto3.dynamodb.types import TypeDeserializer
from app.utils.auth import password_hash

aws_region = os.getenv('AWS_DEFAULT_REGION')

dynamodb = boto3.resource('dynamodb',region_name=aws_region)
global_table = dynamodb.Table('Patients')


class Patient:
    def __init__(self):
        self.table = global_table
        self.deserializer = TypeDeserializer()

    def create_patient(self, user_name, name, contact_number, email, role, DOB,
                       gender, address, password):
        record_id= str(uuid4())
        hashed_password = password_hash(password)
        item = {
            "user_name": user_name,
            "name": name,
            "contact_number": contact_number,
            "email": email,
            "role": role,
            "DOB": DOB,
            "gender": gender,
            "address": address,
            "doctors": [],
            "password": hashed_password,
            "room_id": record_id,
        }
        response = global_table.put_item(Item=item)
        return response

    @classmethod
    def get_all_patients(cls):
        response = global_table.scan()
        items = response.get('Items', [])
        return [cls().deserialize(item) for item in items]

    @classmethod
    def get_patient_by_username(cls, username):
        response = global_table.query(
            KeyConditionExpression="user_name = :val",
            ExpressionAttributeValues={
                ":val": username
            }
        )
        items = response.get('Items', [])
        if items:
            return cls().deserialize(items[0])
        return None

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

    @classmethod
    def update_patient(cls, username, **kwargs):
        # Fetch the doctor object by username
        patient = cls.get_patient_by_username(username)
        if not patient:
            return {'message': 'Patient not found'}

        # Update the patient object with the provided attributes
        for key, value in kwargs.items():
            if key in patient:
                # Convert float values to Decimal
                if isinstance(value, float):
                    value = decimal.Decimal(str(value))
                patient[key] = value
            else:
                return {'message': f'Attribute {key} does not exist'}

        # Print the patient object for debugging
        print("Updated Patient Object:", patient)

        # Save the updated patient object to the database
        try:
            response = cls().table.put_item(Item=patient)
            return {'message': 'Patient updated successfully', 'data': response}
        except Exception as e:
            # Handle any exceptions that may occur during the database operation
            return {'message': 'Failed to update patient', 'error': str(e)}

    @classmethod
    def get_room_id_by_username(cls, username):
        response = global_table.query(
            KeyConditionExpression="user_name = :val",
            ExpressionAttributeValues={
                ":val": username
            }
        )
        items = response.get('Items', [])
        if items:
            return items[0].get('room_id')
        return None