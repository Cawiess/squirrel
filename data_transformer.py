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
                        "jobs": []

                    }
                    
                    
                for job in job_list:
                    self.organization_centric_data[organization]['jobs'].append({
                        "job_title": job[0],
                        "job_location": country,
                        "job_closing_date": job[1],
                        "job_description": job[2]
                    })

                

    def get_transformed_data(self):
        return self.organization_centric_data