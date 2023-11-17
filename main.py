from data_collector import JobScraper
from data_transformer import DataTransformer, load_extracted_organizations
from connect_mongo import MongoDBConnector

from config import countries, pages, export_file_name, extracted_organizations_json, uri, db_name, collection_name

def main():
    print("Scraping organizations...")
    #scraper = JobScraper(countries, pages)
    #scraper.scrape_jobs()
    #scraper.export_data(export_file_name)
    print('Done')

    # Formatting data for insertion into database
    print('running data transformer')
    transformer = DataTransformer(load_extracted_organizations(extracted_organizations_json))
    transformer.transform_data()
    transformer.get_transformed_data()
    print('Done')

    # Inserting one organization into database
    db_connector = MongoDBConnector(uri, db_name, collection_name)
    print(db_connector.list_databases())
    print(db_connector.list_collections())

    one_organization_document = transformer.get_transformed_data()['NRC - Norwegian Refugee Council']
    db_connector.insert_organization(one_organization_document)
    #print(db_connector.show_first_document())
    print(db_connector.find_organization('NRC - Norwegian Refugee Council'))


    
if __name__ == '__main__':
    main()