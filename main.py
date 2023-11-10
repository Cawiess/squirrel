from data_collector import JobScraper

from config import countries, pages, export_file_name

def main():
    "Scraping organizations..."
    scraper = JobScraper(countries, pages)
    scraper.scrape_jobs()
    scraper.export_data(export_file_name)
    
if __name__ == '__main__':
    main()