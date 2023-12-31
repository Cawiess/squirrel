# 172.22.0.2
#uri = 'mongodb://rootuser:rootpass@localhost:27017/'


from pymongo import MongoClient
import json

class MongoDBConnector:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_organization(self, organization):
        """Inserts a single organization document into MongoDB."""
        self.collection.insert_one(organization)

    def insert_all_organizations(self, organization_centric_data):
        for organization, information in organization_centric_data.items():
            self.collection.insert_one(information)


    def list_databases(self):
        """Lists all databases in the MongoDB server."""
        return self.client.list_database_names()
    
    def list_collections(self):
        """Lists all collections in the current database."""
        return self.db.list_collection_names()

    def show_first_document(self):
        """Shows the first document in the current collection."""
        return self.collection.find_one()
    
    def find_organization(self, organization_name):
        query = {"organization_name": organization_name}
        results = self.collection.find(query)

        return results
    
    def count_organizations(self):
        """Counts the number of organization documents in the MongoDB collection."""
        return self.collection.count_documents({})

    # You might also want to add a method to connect to a different database/collection
    def switch_database(self, db_name, collection_name):
        """Switches the current database and collection."""
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    # And possibly a method to close the connection when done
    def close_connection(self):
        """Closes the MongoDB connection."""
        self.client.close()

    def setup_organizations_db(self):
            """Sets up the 'organizations' database."""
            # Check if 'organizations' database exists
            if 'organizations' in self.client.list_database_names():
                # Drop the database if it exists
                self.client.drop_database('organizations')

            # Create a new 'organizations' database with a collection 'organization_data'
            self.switch_database('organizations', 'organization_data')
            # The creation of a collection is implicit, so no need for explicit creation


    def list_countries_of_operation(self, organization_name):
        """Lists the country names of operation for a given organization."""
        query = {"organization_name": organization_name}
        result = self.collection.find_one(query)

        country_names = []
        if result and "countries_of_operation" in result:
            for country in result["countries_of_operation"]:
                if "country_name" in country:
                    country_names.append(country["country_name"])

        return country_names