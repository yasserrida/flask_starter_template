from pymongo import MongoClient


class MongoDBSingleton:
    """MongoDB Singleton"""

    _instances = {}

    def __new__(cls, mongo_url, database_name, collection_name, *args, **kwargs):
        key = (mongo_url, database_name, collection_name)
        if key not in cls._instances:
            cls._instances[key] = super().__new__(cls, *args, **kwargs)
            cls._instances[key].init_connection(
                mongo_url, database_name, collection_name
            )
        return cls._instances[key]

    def init_connection(self, mongo_url, database_name, collection_name):
        """Init connection to MongoDB

        Args:
            mongo_url (str)
            database_name (str)
            collection_name (str)
        """

        self.client = MongoClient(mongo_url)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def get_collection(self):
        """Get collection from MongoDB"""
        return self.collection
