from pymongo import MongoClient

DATABASE = MongoClient()['smep'] # DB_NAME
DEBUG = True
client = MongoClient('localhost', 27017)