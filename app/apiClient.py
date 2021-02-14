#Provides functionality to perform requests on the ClinicalTrials.gov Api
import requests
from enum import Enum

#Usage
'''
- import it 
apiClient = ApiClient()

trials = apiClient.getTrialsFor(age = 29, location = "California",sex = GenderEnum.male.value, isHealthy = HealthyVolunteersEnum.healthy.value) 

for trial in trials:
    print(trial.briefTitle)

#Trial object property: 
- NCTid
- briefTitle
- brief summary
- organization
- conditions (list of strings)

- minimum age
- maximum age
- eligibility criterias (list of criterias to be elegible - i.e list of string)

- url (resolved with the NCTid)

- locationState
- locationCity
- locationFacility

- status
-phase

'''

class GenderEnum(Enum):
    male = "Male"
    female = "Female"

class HealthyVolunteersEnum(Enum):
    healthy = "Accepts Healthy Volunteers"
    notHealthy = "No"

class ApiClient:

    #Returns a list of trials object
    def getTrialsFor(self, age: int, sex: GenderEnum, location: str, isHealthy: HealthyVolunteersEnum, max_trials = 100):

        params = {
            'expr' : f'prostate cancer {location} AND AREA[HealthyVolunteers]"{isHealthy.value}" AND (AREA[Gender]"{sex.value}" OR Area[Gender]"All") AND SEARCH[Location](AREA[LocationCountry]United States AND AREA[LocationStatus]Recruiting)',
            'fmt' : 'JSON',
            'max_rnk': max_trials
        }

        jsonResponse = self.createRequest(params)
        trialsArray = []
        
        try :
            if study['Study']['ProtocolSection']['EligibilityModule']['EligibilityCriteria']:
                eligibilityCriterias = study['Study']['ProtocolSection']['EligibilityModule']['EligibilityCriteria'].splitlines()
            else:
                eligibilityCriterias = "No data available"
        except:
            eligibilityCriterias = "No data available"

        try:
            if jsonResponse['FullStudiesResponse']['FullStudies']:
                for study in jsonResponse['FullStudiesResponse']['FullStudies']:
                    decodedStudy = self.decodeJSON(study)
                    

                    if self.isAgeMatching(age, int(decodedStudy.minimumAge), int(decodedStudy.maximumAge)):
                        trialsArray.append(decodedStudy)
            else:
                trialsArray = []
        except:
            trialsArray = []

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
        briefSummary = study['Study']['ProtocolSection']['DescriptionModule']['BriefSummary']

        status = study['Study']['ProtocolSection']['StatusModule']['OverallStatus']

        #get phases
        try:
            if study['Study']['ProtocolSection']['DesignModule']['PhaseList']['Phase']:
                phase = study['Study']['ProtocolSection']['DesignModule']['PhaseList']['Phase'][0]
            else:
                phase = "No data Available"
        except: 
            phase = "No data Available"

        #get eligibilityCriterias
        try :
            if study['Study']['ProtocolSection']['EligibilityModule']['EligibilityCriteria']:
                eligibilityCriterias = study['Study']['ProtocolSection']['EligibilityModule']['EligibilityCriteria'].splitlines()
            else:
                eligibilityCriterias = "No data available"
        except:
            eligibilityCriterias = "No data available"

        #get minimumAge
        try:
            if study['Study']['ProtocolSection']['EligibilityModule']['MinimumAge']:
                    minumumAge = study['Study']['ProtocolSection']['EligibilityModule']['MinimumAge'].rstrip('Years')                        
            else:
                minumumAge = "-1"
        except:
                minumumAge = "-1"

        #get maximumAge
        try:
            if study['Study']['ProtocolSection']['EligibilityModule']['MaximumAge']:
                    maximumAge = study['Study']['ProtocolSection']['EligibilityModule']['MaximumAge'].rstrip('Years')                        
            else:
                maximumAge = "101"
            
        except:
                maximumAge = "101"

        locationState = study['Study']['ProtocolSection']['ContactsLocationsModule']['LocationList']['Location'][0]['LocationState']

        #Contact Details of Location
        try:
            if study['Study']['ProtocolSection']['ContactsLocationsModule']['LocationList']['Location']:

                locationState = study['Study']['ProtocolSection']['ContactsLocationsModule']['LocationList']['Location'][0]['LocationState']
                locationCity = study['Study']['ProtocolSection']['ContactsLocationsModule']['LocationList']['Location'][0]['LocationCity']
                locationFacility = study['Study']['ProtocolSection']['ContactsLocationsModule']['LocationList']['Location'][0]['LocationFacility']

            else:
                locationState = "No data Available"
                locationCity = "No data Available"
                locationFacility = "No data Available"
        except:
            locationState = "No data Available"
            locationCity = "No data Available"
            locationFacility = "No data Available"
        
        trial = Trial(NCTid = NCTid, 
                briefTitle = briefTitle,
                briefSummary = briefSummary,
                organization = organization, 
                conditions = conditions, 
                locationState = locationState,
                locationCity = locationCity,
                locationFacility = locationFacility,
                minimumAge = minumumAge,
                maximumAge = maximumAge,
                eligibilityCriterias = eligibilityCriterias,
                status = status,
                phase = phase
            )

        return trial
    
    #Check if the age inserted by the user is greater than minimum age 
    def isAgeMatching(self, age: int, minumumAge: int, maximumAge: int) -> bool:
        
        if age > minumumAge and age < maximumAge:
            return True
        else:
            return False
        

#Model
class Trial:

    def __init__(self, NCTid: str, briefTitle: str, organization, conditions: [str], briefSummary: str, locationState: str, locationCity: str, locationFacility: str, minimumAge: int, maximumAge: int, eligibilityCriterias: [str], status: str, phase: str):
        
        self.NCTid = NCTid
        self.briefTitle = briefTitle
        self.briefSummary = briefSummary
        self.conditions = conditions
        self.organization = organization

        self.eligibilityCriterias = eligibilityCriterias

        self.url = f"https://clinicaltrials.gov/ct2/show/{NCTid}"
        self.minimumAge = minimumAge
        self.maximumAge = maximumAge

        #Location information
        self.locationState = locationState
        self.locationCity = locationCity
        self.locationFacility = locationFacility

        self.status = status
        self.phase = phase
        

if __name__ == "__main__":
    apiClient = ApiClient()
    studies = apiClient.getTrialsFor(age = 35, location = "California" , sex = GenderEnum.male, isHealthy = HealthyVolunteersEnum.healthy)
    for study in studies:
        print("STUDY: ")
        print(f"phase: {study.phase} - status: {study.status}")
        print('--------------')