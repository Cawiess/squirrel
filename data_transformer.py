# The purpose of the DataTransformer class is to strucure the data according to the data schema defined for the MongoDB database.
# See schema in data schema.txt

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

                country_job_data = {"country_name": country, "jobs": job_list}
                self.organization_centric_data[organization]["countries"].append(country_job_data)

    def get_transformed_data(self):
        return self.organization_centric_data
