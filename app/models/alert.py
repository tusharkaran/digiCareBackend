import boto3
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.resource('dynamodb')
global_table = dynamodb.Table('alerts')


class Alert:
    def __init__(self):
        self.table = global_table
        self.deserializer = TypeDeserializer()

    def create_alert(self, patient, doctor, timestamp, severity, description):
        item = {
            "patient": patient,
            "doctor": doctor,
            "timestamp": str(timestamp),
            "severity": severity,
            "description": description
        }
        response = global_table.put_item(Item=item)
        return response

    @classmethod
    def get_alert_by_id(cls, alert_id):
        response = global_table.get_item(
            Key={
                'alert_id': alert_id
            }
        )
        item = response.get('Item')
        if item:
            return cls().deserialize(item)
        return None

    @classmethod
    def deserialize(cls, item):
        if isinstance(item, dict):
            return {key: cls.deserialize(value) for key, value in item.items()}
        elif isinstance(item, list):
            return [cls.deserialize(value) for value in item]
        else:
            return item
