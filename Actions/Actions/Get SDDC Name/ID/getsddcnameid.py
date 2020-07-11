import requests
import json
import urllib3


api_base_url = 'https://vmc.vmware.com/vmc/api'
refresh_token = ""
ORG_ID = ""
headers = {'Content-Type': 'application/json'}


def get_token():
      api_url = 'https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize?refresh_token={0}'.format(refresh_token)
      response = requests.post(api_url, headers=headers, verify=False)
      if response.status_code == 200:
          json_data = json.loads(response.content.decode('utf-8'))
          key = json_data['access_token']
          return key
      else:
          return None
access_key = get_token()
headers1 = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(access_key)}

def getSDDC(ORG_ID, access_key):
    api_url = '{0}/orgs/{1}/sddcs'.format(api_base_url,ORG_ID)
    myHeader = {'csp-auth-token': access_key}
    sddcList = requests.get(api_url, headers = myHeader, verify = False)
    for i in sddcList.json():
        print("ID: " + i['name'])
        print("Name: " + i['id'])

def handler(context, inputs):
    access_key = get_token()
    getSDDC(ORG_ID, access_key)
