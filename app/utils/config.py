from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# class Config:
#     DEBUG = False
#     TESTING = False
#
#     # MongoDB Configuration
#     MONGODB_SETTINGS = {
#         'db': 'digicare_database',
#         'host': 'mongodb://localhost:27017/digicare_database'
#     }
#
#     # Additional configurations can be added as needed
#
# # Create a new client and connect to the server
# client = MongoClient(Config.MONGODB_SETTINGS['host'], server_api=ServerApi('1'))
#
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     raise e