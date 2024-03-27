import uuid

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.resource('dynamodb')
global_table = dynamodb.Table('realtime-recording')


class HealthRecord:
    def __init__(self):
        self.table = global_table
        self.deserializer = TypeDeserializer()

    def create_health_record(self, patient_username, timestamp, records):
        item = {
            "Recording_id": str(uuid.uuid4()),
            "patient_username": patient_username,
            "timeStamp": str(timestamp),
            "records": records
        }
        response = global_table.put_item(Item=item)
        return response

    @classmethod
    def get_health_record_by_patient(cls, patient_username, sort_by_timestamp=True):
        response = global_table.query(
            KeyConditionExpression="patient_username = :val",
            ExpressionAttributeValues={
                ":val": patient_username
            },
            ScanIndexForward=not sort_by_timestamp  # Sort in descending order if True
        )
        items = response.get('Items', [])
        if items:
            return [cls().deserialize(item) for item in items]
        return None

    @classmethod
    def update_health_record(cls, Recording_id, records):
        response = global_table.update_item(
            Key={
                'Recording_id': Recording_id
            },
            UpdateExpression="set records = :r",
            ExpressionAttributeValues={
                ':r': records
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    @classmethod
    def delete_health_record(cls, Recording_id):
        response = global_table.delete_item(
            Key={
                'Recording_id': Recording_id
            }
        )
        return response

    @classmethod
    def deserialize(cls, item):
        if isinstance(item, dict):
            return {key: cls.deserialize(value) for key, value in item.items()}
        elif isinstance(item, list):
            return [cls.deserialize(value) for value in item]
        else:
            return item

    @classmethod
    def get_latest_health_record(cls, patient_username):
        response = global_table.query(
            KeyConditionExpression=Key('patient_username').eq(patient_username),
            ScanIndexForward=False,  # Sort in descending order by default timestamp
            Limit=1  # Retrieve only the latest record
        )
        items = response.get('Items', [])
        if items:
            return cls().deserialize(items[0])
        return None