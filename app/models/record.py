import decimal

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import TypeDeserializer
# from simulation import HealthRecorder

dynamodb = boto3.resource('dynamodb')
global_table = dynamodb.Table('Recorded_Data')


class RecordedData:
    def __init__(self):
        self.table = global_table
        self.deserializer = TypeDeserializer()

    def create_record(self, record_id, patient_username, timestamp, blood_pressure, heart_rate, o2, temperature):
        item = {
            "record_id": record_id,
            "patient_username": patient_username,
            "timestamp": timestamp,
            "blood_pressure": blood_pressure,
            "heart_rate": heart_rate,
            "o2": o2,
            "temperature": temperature
        }
        response = self.table.put_item(Item=item)
        return response

    @classmethod
    def get_record_by_id(cls, record_id):
        response = global_table.get_item(
            Key={
                'record_id': record_id
            }
        )
        item = response.get('Item')
        if item:
            return cls().table.deserialize(item)
        return None

    @classmethod
    def get_all_records(cls):
        response = global_table.scan()
        items = response.get('Items', [])
        return [cls().deserialize(item) for item in items]

    @classmethod
    def get_records_by_patient_username(cls, patient_username):
        response = global_table.scan(
            FilterExpression='patient_username = :val',
            ExpressionAttributeValues={
                ':val': patient_username
            }
        )
        items = response.get('Items', [])
        records = [cls.deserialize(item) for item in items]
        return records

    @classmethod
    def deserialize(cls, item):
        if isinstance(item, dict):
            return {key: cls.deserialize(value) for key, value in item.items()}
        elif isinstance(item, list):
            return [cls.deserialize(value) for value in item]
        else:
            return item

    @classmethod
    def get_latest_record(cls, patient_username):
        response = global_table.scan(
            FilterExpression='patient_username = :val',
            ExpressionAttributeValues={
                ':val': patient_username
            }
        )
        items = response.get('Items', [])
        if items:
            # Sort items by timestamp (assuming timestamp is stored as a string)
            sorted_items = sorted(items, key=lambda x: x['timestamp'], reverse=True)
            latest_record = cls.deserialize(sorted_items[0])
            return latest_record
        return None

    # @classmethod
    # def generate_latest_record_data(cls):
    #     return HealthRecorder.send_recorded_parameters()