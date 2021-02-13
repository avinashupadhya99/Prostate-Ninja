#Provides functionality to perform requests on the ClinicalTrials.gov Api

import requests

class ApiClient:
    
    #Returns a list of trials object
    def getTrialsFor(self, age, sex, isHealthy, max_trials):

        params = {
            'expr' : 'heart attack AND SEARCH[Location](AREA[LocationCountry]United States AND AREA[LocationStatus]Recruiting)',
            'fmt' : 'JSON',
            'max_rnk': 20
        }

        jsonResponse = self.createRequest(params)

        return jsonResponse

    #Run the request on the API with the specified parameters and returns a JSON file
    def createRequest(self, params):

        baseURL = "https://clinicaltrials.gov/api/query/full_studies?" #Check other available endpoints here https://clinicaltrials.gov/api/gui/ref/api_urls
        response = requests.get(baseURL, params = params)
        jsondata = response.json()

        return jsondata


client = ApiClient()

#Class for 
class Trial:

    def __init__(self, NTCid, briefTitle, organization, condition, locationContactPhone, locationContactEmail):
        self.NTCid = NTCid
        self.briefTitle = briefTitle
        self.condition = condition
        self.locationContactEmail = locationContactEmail
    