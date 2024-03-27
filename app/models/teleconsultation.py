import boto3
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.resource('dynamodb')
global_table = dynamodb.Table('teleconsultation')


class Teleconsultation:
    def __init__(self):
        self.table = global_table
        self.deserializer = TypeDeserializer()

    def create_teleconsultation(self, patient, doctor, platform, scheduled_time):
        item = {
            "patient": patient,
            "doctor": doctor,
            "platform": platform,
            "scheduled_time": str(scheduled_time)
        }
        response = self.table.put_item(Item=item)
        return response

    @classmethod
    def get_teleconsultation_by_id(cls, record_id):
        response = global_table.get_item(
            Key={
                'record_id': record_id
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
