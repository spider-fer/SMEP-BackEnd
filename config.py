from pymongo import MongoClient

DATABASE = MongoClient()['smep'] # DB_NAME
DEBUG = True
#Uncomment the next line to use docker container
#client = MongoClient('mongodb://db:27017/dockerdemo', 27017)
client = MongoClient('localhost', 27017)