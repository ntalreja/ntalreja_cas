import requests                         # need this for Get/Post/Delete
import json

strProdURL = "https://vmc.vmware.com"

def getAccessToken(myKey):
    params = {'refresh_token': myKey}
    headers = {'Content-Type': 'application/json'}
    response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize', params=params, headers=headers)
    jsonResponse = response.json()
    access_token = jsonResponse['access_token']
    return access_token
    
def createSDDC(name, region, hosts, tenantid, sessiontoken):
    myHeader = {'csp-auth-token': sessiontoken}
    myURL = strProdURL + "/vmc/api/orgs/" + tenantid + "/sddcs"
    strRequest = {
        "num_hosts": hosts,
        "name": name,
        "provider": "ZEROCLOUD",
        "region": region}
    response = requests.post(myURL, json=strRequest, headers=myHeader)
# debug only
    #print("result =" + str(response.status_code))
    jsonResponse = response.json()

    if str(response.status_code) != "202":
        print("\nERROR: " + str(jsonResponse['error_messages'][0]))

    return

# add token of your SDDC
Refresh_Token = ""

ORG_ID = ""
    
def handler(context, inputs):
    numHosts    = inputs["number_hosts"]
    targetRegion = inputs["targetRegion"]
    sddcName = inputs["sddcName"]
    sessiontoken = getAccessToken(Refresh_Token)
    createSDDC(sddcName, targetRegion, numHosts, ORG_ID, sessiontoken)