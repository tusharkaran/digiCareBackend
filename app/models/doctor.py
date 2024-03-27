import decimal

import boto3
from boto3.dynamodb.types import TypeDeserializer
from app.utils.auth import password_hash

dynamodb = boto3.resource('dynamodb')
global_table = dynamodb.Table('doctors')


class Doctor:
    def __init__(self):
        self.table = global_table
        self.deserializer = TypeDeserializer()

    def create_doctor(self, user_name, name, contact_number, email, role, DOB, gender, address, start_year_of_practice,
                      specialization, study_history, password, Hospital):
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
            "start_year_of_practice": start_year_of_practice,
            "availability_hours": [],
            "specialization": specialization,
            "study_history": study_history,
            "patients": [],
            "password": hashed_password,
            "Hospital": Hospital
        }
        response = self.table.put_item(Item=item)
        return response

    @classmethod
    def get_all_doctors(cls):
        response = global_table.scan()
        items = response.get('Items', [])
        return [cls().deserialize(item) for item in items]

    @classmethod
    def get_doctor_by_username(cls, username):
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
    def update_doctor(cls, username, **kwargs):
        # Fetch the doctor object by username
        doctor = cls.get_doctor_by_username(username)
        if not doctor:
            return {'message': 'Doctor not found'}

        # Update the doctor object with the provided attributes
        for key, value in kwargs.items():
            if key in doctor:
                # Convert float values to Decimal
                if isinstance(value, float):
                    value = decimal.Decimal(str(value))
                doctor[key] = value
            else:
                return {'message': f'Attribute {key} does not exist'}

        # Print the doctor object for debugging
        print("Updated Doctor Object:", doctor)

        # Save the updated doctor object to the database
        try:
            response = cls().table.put_item(Item=doctor)
            return {'message': 'Doctor updated successfully', 'data': response}
        except Exception as e:
            # Handle any exceptions that may occur during the database operation
            return {'message': 'Failed to update doctor', 'error': str(e)}

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
