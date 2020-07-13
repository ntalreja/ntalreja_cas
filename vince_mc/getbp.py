import json
import requests
import time
import urllib3
urllib3.disable_warnings()
api_url_base = 'https://api.mgmt.cloud.vmware.com/'
headers = {'Content-Type': 'application/json'}
refresh_token = ''
def extract_values(obj, key):
  """Pull all values of specified key from nested JSON."""
  arr = []
  def extract(obj, arr, key):
    """Recursively search for values of key in JSON tree."""
    if isinstance(obj, dict):
      for k, v in obj.items():
        if isinstance(v, (dict, list)):
          extract(v, arr, key)
        elif k == key:
          arr.append(v)
    elif isinstance(obj, list):
      for item in obj:
        extract(item, arr, key)
    return arr
  results = extract(obj, arr, key)
  return results
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
headers1 = {'Content-Type': 'application/json',
      'Authorization': 'Bearer {0}'.format(access_key)}

def get_blueprints():
  api_url = '{0}blueprint/api/blueprints'.format(api_url_base)
  response = requests.get(api_url, headers=headers1, verify=False)
  if response.status_code == 200:
      json_data = json.loads(response.content.decode('utf-8'))
      print('Successfully Launched vRA 8 Field Demo Nightly Build')
  else:
    return None
  print(response.text)
get_blueprints()