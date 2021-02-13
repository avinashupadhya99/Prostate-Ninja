#Provides functionality to perform requests on the ClinicalTrials.gov Api

import requests

class ApiClient:

    #Returns a list of trials object
    def getTrialsFor(self, age, sex, isHealthy, max_trials):

        params = {
            'expr' : 'prostate cancer AND SEARCH[Location](AREA[LocationCountry]United States AND AREA[LocationStatus]Recruiting)',
            'fmt' : 'JSON',
            'max_rnk': 20
        }

        jsonResponse = self.createRequest(params)
        trialsArray = []
        for study in jsonResponse['FullStudiesResponse']['FullStudies']:
            decodedStudy = self.decodeJSON(study)
            trialsArray.append(decodedStudy)

        return trialsArray
            
    #Run the request on the API with the specified parameters and returns a JSON file
    def createRequest(self, params):

        baseURL = "https://clinicaltrials.gov/api/query/full_studies?" #Check other available endpoints here https://clinicaltrials.gov/api/gui/ref/api_urls
        response = requests.get(baseURL, params = params)
        jsondata = response.json()

        return jsondata

    #Decode the Json and create the trial object
    def decodeJSON(self,study):

        NCTid = study['Study']['ProtocolSection']['IdentificationModule']['NCTId']
        briefTitle = study['Study']['ProtocolSection']['IdentificationModule']['BriefTitle']
        organization = study['Study']['ProtocolSection']['IdentificationModule']['Organization']['OrgFullName']
        conditions = study['Study']['ProtocolSection']['ConditionsModule']['ConditionList']['Condition']

        #Contact Details of Location
        try:
            if study['Study']['ProtocolSection']['ContactsLocationsModule']['LocationList']['Location']:
                locationState = study['Study']['ContactsLocationsModule']['LocationList']['Location'][0]['LocationState']
            else:
                locationState = "No data Available"

        except:
            locationState = "No data Available"

        trial = Trial(NCTid = NCTid, 
                briefTitle = briefTitle, 
                organization = organization, 
                conditions = conditions, 
                locationState = locationState
            )

        return trial


#Model
class Trial:

    def __init__(self, NCTid, briefTitle, organization, conditions, locationState):
        self.NCTid = NCTid
        self.briefTitle = briefTitle
        self.conditions = conditions
        self.locationState = locationState
        self.url = f"https://clinicaltrials.gov/ct2/show/{NCTid}"


apiClient = ApiClient()
print(apiClient.getTrialsFor(14,2,3,10)[0].NCTid)
print(apiClient.getTrialsFor(14,2,3,10)[0].briefTitle)