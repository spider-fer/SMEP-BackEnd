from pymongo import MongoClient

DATABASE = MongoClient()['smep'] # DB_NAME
DEBUG = True
client = MongoClient('mongodb://db:27017/dockerdemo', 27017)