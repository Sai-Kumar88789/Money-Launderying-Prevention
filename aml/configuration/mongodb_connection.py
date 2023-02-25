import pymongo 
from aml.constant.database import DATABASE_NAME
from aml.constant.env_variable import MONGODB_URL_KEY
from dotenv import load_dotenv
import certifi
import os
ca = certifi.where()
load_dotenv()

class MongodbClient:
    client = None
    def __init__(self,database_name = DATABASE_NAME) -> None:
        try:
            if MongodbClient.client is None:
                mongodb_url = os.getenv(MONGODB_URL_KEY)
                MongodbClient.client =pymongo.MongoClient(mongodb_url,tlsCAFile =ca )
            self.client = MongodbClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e 
        