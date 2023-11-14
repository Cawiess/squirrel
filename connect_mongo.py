# 172.22.0.2
#uri = 'mongodb://rootuser:rootpass@localhost:27017/'


from pymongo import MongoClient

class MongoDBConnector:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_organization(self, organization):
        """Inserts a single organization document into MongoDB."""
        self.collection.insert_one(organization)

    def list_databases(self):
        """Lists all databases in the MongoDB server."""
        return self.client.list_database_names()

    # You might also want to add a method to connect to a different database/collection
    def switch_database(self, db_name, collection_name):
        """Switches the current database and collection."""
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    # And possibly a method to close the connection when done
    def close_connection(self):
        """Closes the MongoDB connection."""
        self.client.close()


uri = 'mongodb://rootuser:rootpass@localhost:27017/'

db_name = 'organizations'
collection_name = 'organization_data'

db_connector = MongoDBConnector(uri, db_name, collection_name)
print(db_connector.list_databases())
db_connector.close_connection()
