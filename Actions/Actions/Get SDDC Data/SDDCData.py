import requests                         # need this for Get/Post/Delete
import json



strProdURL = "https://vmc.vmware.com"
# add token of your Zero Cloud SDDC
Refresh_Token = ""
# add Org of your Zero Cloud SDDC
ORG_ID = ""
# add Zero Cloud SDDC ID 
SDDC_ID = ""

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
