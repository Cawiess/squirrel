from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import json

from config import countries, export_file_name, pages

class JobScraper:
    def __init__(self, countries, pages):
        self.countries = countries
        self.pages = pages
        self.extracted_organizations = {country: {} for country in countries} # each country has a dict containing job data
    
    ## Helper functions ##
    
    @staticmethod
    def has_numbers(string):
        return any(char.isdigit() for char in string)
    
    @staticmethod
    def date_pruner(string):
        '''
        String: Date as formatted at Impactpool.
        There are some special cases:
         - Closing tomorrow, closing today, closing in X days
        '''

        if string.lower() == 'closing today':
            closing_date = datetime.today()
        elif string.lower() == 'closing tomorrow':
            closing_date = datetime.today() + timedelta(days=1)
        elif JobScraper.has_numbers(string):
            try:
                string = string.lower().replace('closing', '').replace('of', '').split()

                s = ''.join([str(''.join(filter(str.isdigit, string[0]))), ' ', string[1], ' ', str(datetime.now().year)])
                closing_date = datetime.strptime(s, '%d %B %Y')
            except:
                closing_date = datetime.today() + timedelta(days=7)

        else:
            closing_date = datetime.today() + timedelta(days=int(''.join(filter(str.isdigit, string))))
            closing_date

        return closing_date.date()
    
    @staticmethod
    def fetch_job_description(job_description_link):
        url = f"https://www.impactpool.org{job_description_link}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            job_description = soup.find_all('div', class_='job-description')

        else:
            print(f'Failed to retrieve data: {response.status_code}')

        clean_job_description = [i for i in list(map(lambda x: x.get_text(), job_description[0].find_all(['div', 'p', 'ol' ,'li']))) if i not in ['','\n']]
        clean_job_description = ''.join(clean_job_description)

        return clean_job_description
    
    def scrape_jobs(self):
        for country in self.countries:
            for page in self.pages:
                url = f"https://www.impactpool.org/search?q=&countries%5B%5D={country}&from={page}&q="
                response = requests.get(url)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'lxml')
                    self.process_organization_data(soup, country)
                else:
                    print(f"failde to retreive data: {response.status_code}")

    def process_organization_data(self, soup, country):
        organization_divs = soup.find_all('div', class_='job ip-layout')

        for div in organization_divs:
            organization_name = div.find_all('div', class_='job-organization')[0].get_text().strip()
            if organization_name not in self.extracted_organizations[country].keys():
                self.extracted_organizations[country][organization_name] = []
            try:
                job_title = div.find_all('a', class_='apply-link')[0].get_text()
                job_description_link = div.find_all('a', class_='apply-link')[0].get('href')
                job_description = JobScraper.fetch_job_description(job_description_link)
            except:
                job_title = div.find_all('a', class_='job-description-link')[0].get_text()
                job_description = 'unavailable'

            if len(div.find_all('div', class_='closing-date'))>0:
                closing_date = JobScraper.date_pruner(div.find_all('div', class_='closing-date')[0].get_text())
                #job_description = fetch_job_description(job_description_link)
            else:
                closing_date = 'no date specified'
                #job_description = fetch_job_description(job_description_link)


            #print('-----')
            #print(country)
            #print(organization_name)
            #print(job_title)
            #print(closing_date)
            #print('-----')

            self.extracted_organizations[country][organization_name].append([job_title, closing_date, job_description])
        
    def export_data(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self.extracted_organizations, fp, indent=4, sort_keys=True, default=str)