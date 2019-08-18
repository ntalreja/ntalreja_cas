#import requests
import json
   
def handler(context, inputs):
   print('Action started.')
      
   tags = inputs['tags']
   vmName = inputs["resourceNames"][0]
  
   tag = 'tango-machine'
   if 'Application' in vmName:
       tag = 'Application Tier'
   elif 'DB' in vmName:
       tag = 'DB Tier'
     
   tags[tag] = 'tango-machine'
      
   #print('Tag VM action! tag: "{}".'.format(tag))
      
   #slackMsg = ':label: Is this mine? tag: "' + tag + '".'
   #body = {
   #"channel": "#general",
   #"username": "ABX",
   #"text": slackMsg,
   #"icon_emoji": ":bell:"
   #}
   #requests.post('https://hooks.slack.com/services/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', data=json.dumps(body), verify=False)
 
   return { 'tags' : tags }