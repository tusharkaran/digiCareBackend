import decimal
import os

import boto3
from boto3.dynamodb.types import TypeDeserializer
from app.utils.auth import password_hash

aws_region = os.getenv('AWS_DEFAULT_REGION')

dynamodb = boto3.resource('dynamodb',region_name=aws_region)
global_table = dynamodb.Table('Admin')


class Admin:
    def __init__(self):
        self.table = global_table
        self.deserializer = TypeDeserializer()

    def create_admin(self, user_name, password):
        hashed_password = password_hash(password)
        item = {
            "user_name": user_name,
            "password": hashed_password
        }
        response = global_table.put_item(Item=item)
        return response

    @classmethod
    def get_admin_by_username(cls, username):
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

