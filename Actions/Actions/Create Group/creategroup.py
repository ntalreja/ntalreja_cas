import json
import base64
import requests
import json
import base64
import requests
import time
import os
import traceback
import urllib3
urllib3.disable_warnings()

api_base_url = "https://nsx-xxxxxx"
myHeader = {'Content-Type':'application/json','csp-auth-token':}

def create_group(group_name):
    api_url = '{0}/policy/api/v1/infra/domains/cgw/groups/{1}'.format(api_base_url,group_name)
    payload = {
               "expression" : [ 
                 {
                   "member_type" : "VirtualMachine",
                   "key" : "Tag",
                   "operator" : "EQUALS",
                   "value" : "vRA_Tag",
                   "resource_type" : "Condition"
                 } 
               ],
               "id" : group_name,
               "display_name" : group_name
              }
    response = requests.put(api_url, headers = myHeader, data = json.dumps(payload), verify = False)
    json_response_status_code = response.status_code
    print(response.text.encode('utf8'))

def handler(context, inputs):
    print('Create Group')
    group_name = inputs["group_name"]
    status = create_group(group_name)
    return status