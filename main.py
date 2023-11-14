from data_collector import JobScraper
from data_transformer import DataTransformer, load_extracted_organizations

from config import countries, pages, export_file_name, extracted_organizations_json

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
    
if __name__ == '__main__':
    main()