from dotenv import load_dotenv
from os import environ

print('loading variables...')
load_dotenv()

MONGO_URI = environ.get('MONGO_URI')
MONGO_DATABASE = environ.get('MONGO_DATABASE')

def get_mongo_uri():
    return MONGO_URI

def get_mongo_database():
    return MONGO_DATABASE