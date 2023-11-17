# The purpose of the DataTransformer class is to strucure the data according to the data schema defined for the MongoDB database.
import json

def load_extracted_organizations(json_file):
    with open(f"{json_file}") as file:
        data = json.loads(file.read()) 
        return data

class DataTransformer:
    def __init__(self, extracted_data):
        self.extracted_data = extracted_data
        self.organization_centric_data = {}

    def transform_data(self):
        for country, organizations in self.extracted_data.items():
            for organization, job_list in organizations.items():
                if organization not in self.organization_centric_data:
                    self.organization_centric_data[organization] = {
                        "organization_name": organization, 
                        "countries": []
                    }

                formatted_job_list = []
                for job in job_list:
                    formatted_job_list.append({
                        "job_title": job[0],
                        "closing_date": job[1],
                        "job_description": job[2]
                    })

                country_job_data = {"country_name": country, "jobs": formatted_job_list}
            self.organization_centric_data[organization]["countries"].append(country_job_data)

                

    def get_transformed_data(self):
        return self.organization_centric_data

# Schema for reference
'''
{
    "organization_name" : "name of organization",
    "countries": [
        {
            "country_name": "name of country
            "jobs": [
                {
                    "job_title": "title of job",
                    "closing_date": "yyyy-mm-dd"
                    "job_description": "long string explaining the job..."
                }
            ]
        },
        {
            "country_name": "name of another country
            "jobs": [
                {
                    "job_title": "title of job",
                    "closing_date": "yyyy-mm-dd"
                    "job_description": "long string explaining the job..."
                },
                {
                    "job_title": "title of job",
                    "closing_date": "yyyy-mm-dd"
                    "job_description": "long string explaining the job..."
                }
            ]
        }
    ]
}
'''