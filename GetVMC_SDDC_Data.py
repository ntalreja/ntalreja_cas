import requests                         # need this for Get/Post/Delete
import json



strProdURL = "https://vmc.vmware.com"
# add token of your Zero Cloud SDDC
Refresh_Token = "2rgGMnx7PhZ2Mpz1ooEo2KdVvju79smer4pVRjhb5H6NreeXHa93xa7nFQH5xoWY"
# add Org of your Zero Cloud SDDC
ORG_ID = "2acf4023-1778-4e6a-a892-7635b8c7f4fb"
# add Zero Cloud SDDC ID 
SDDC_ID = "32df704d-d2d4-494b-852e-631011909d4e"

def getAccessToken(myKey):
    params = {'refresh_token': myKey}
    headers = {'Content-Type': 'application/json'}
    response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize', params=params, headers=headers)
    jsonResponse = response.json()
    access_token = jsonResponse['access_token']
    return access_token
    
def get_sddc(ORG_ID, sessiontoken):
    myHeader = {'csp-auth-token': sessiontoken}
    myURLS = strProdURL + "/vmc/api/orgs/" + ORG_ID + "/sddcs/"
    sddcList = requests.get(myURLS, headers=myHeader)
    if sddcList.status_code != 200:
        print('API Error')
    else:
        for sddc in sddcList.json():
            print("SDDC Name: " + sddc['name'])
            print("SDDC Create Date: " + sddc['created'])
            print("SDDC Provider: " + sddc['provider'])
            print("SDDC Region: " + sddc['resource_config']['region'])
            
def handler(context, inputs):
    sessiontoken = getAccessToken(Refresh_Token)
    get_sddc(ORG_ID, sessiontoken)