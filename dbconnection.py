'''Connection to database'''
from pymongo import MongoClient

class DB:
    def __init__(self):
        MONGO_URI ="mongodb://127.0.0.1:27017/" 
        DATABASE="test"
        self.client = MongoClient(MONGO_URI)
        self.connection= self.client.get_database(DATABASE)
        pass
    def save(self, data):
        '''Save data into db'''
        return self.connection.table.insert_one(data)

db = DB()
