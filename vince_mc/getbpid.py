def get_blueprints():
  api_url = '{0}blueprint/api/blueprints'.format(api_url_base)
  response= requests.get(api_url, headers=headers1, verify=False)
  data = json.loads(response.content)
  for i in data['content']:
      print("Name " + i['name'])
      print("ID " + i['id'])
get_blueprints()