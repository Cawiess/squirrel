# This file contains configurations, parameters and environment variables used throughout the modules.

from datetime import datetime, timedelta

'''
countries = ['Jordan', 
             'Syria', 
             'Lebanon', 
             'Egypt', 
             'Palestinian+Territory', 
             'Iraq', 
             'Libya', 
             'Tunisia', 
             'Algeria',
             'Morocco', 
             'Yemen', 
             'Saudi+Arabia',
             'United+Arab+Emirates', 
             'Qatar', 
             'Bahrain', 
             'Kuwait', 
             'Israel']
'''

countries = ['Jordan']

pages = [0, 40, 80] #represent number of results to show. To get around the "Show more button".

export_file_name = f"extracted_organizations_export_{datetime.today().strftime('%d-%m-%Y')}.json"

extracted_organizations_json = 'extracted_organizations_export_14-11-2023.json' # raw json data for use in DataTransformer