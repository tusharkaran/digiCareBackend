import decimal
import os
import uuid

import boto3
from boto3.dynamodb.types import TypeDeserializer
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Attr


aws_region = os.getenv('AWS_DEFAULT_REGION')

dynamodb = boto3.resource('dynamodb', region_name=aws_region)
global_table = dynamodb.Table('timeSlot')


class TimeSlot:
    def __init__(self):
        self.table = global_table
        self.deserializer = TypeDeserializer()

    def generate_slot_start_times(start_time, end_time):
        start_datetime = datetime.strptime(start_time, '%H:%M')
        end_datetime = datetime.strptime(end_time, '%H:%M')
        interval = timedelta(minutes=15)

        current_datetime = start_datetime
        while current_datetime + interval <= end_datetime:  # Ensure slot doesn't extend beyond end time
            yield current_datetime.strftime('%H:%M')
            current_datetime += interval

    @classmethod
    def createTimeSlot(self, username, start_time,end_time, day_name):

        slots = self.generate_slot_start_times(start_time, end_time)
        created_slots = []
        for slot_start_time in slots:
            item = {
                "id": str(uuid.uuid4()),
                "start_time": slot_start_time,
                "is_booked": False,
                "day_name": day_name,
                "parent_start_time": start_time,
                "parent_end_time": end_time,
                "doctor_username": username
            }
            response = global_table.put_item(Item=item)
            created_slots.append(response)
        return created_slots

    @classmethod
    def get_time_slots_by_doctor_username(cls, username):
        response = global_table.scan(
            FilterExpression='doctor_username = :val',
            ExpressionAttributeValues={
                ':val': username
            }
        )
        items = response.get('Items', [])
        return [cls().deserialize(item) for item in items]

    @classmethod
    def get_time_slots_by_doctor_username_day(cls, username, day_name):
        response = global_table.scan(
            FilterExpression='doctor_username = :val AND day_name = :day',
            ExpressionAttributeValues={
                ':val': username,
                ':day': day_name
            }
        )
        items = response.get('Items', [])
        return [cls().deserialize(item) for item in items]

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
    def delete_all_time_slots(cls):
        response = global_table.scan()
        items = response.get('Items', [])
        for item in items:
            key = {k['AttributeName']: item[k['AttributeName']] for k in global_table.key_schema}
            print("Deleting item with key:", key)  # Debugging
            global_table.delete_item(Key=key)
        return [cls().deserialize(item) for item in items]

    @classmethod
    def delete_time_slots(cls, time_slots):
        for item in time_slots:
            key = {k['AttributeName']: item[k['AttributeName']] for k in global_table.key_schema}
            print("Deleting item with key:", key)  # Debugging
            global_table.delete_item(Key=key)

        return [cls().deserialize(item) for item in time_slots]

