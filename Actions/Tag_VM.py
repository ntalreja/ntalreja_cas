#use elif statement to define the tag, if vmName has some text then use a certain tag 
#make sure to add the vmName_VM to the resourceNames section

import requests
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
   elif 'Dev' in vmName:
       tag = "Dev Machine"
   elif 'Apache' in vmName:
       tag = "apache machine"
     
   tags[tag] = 'tango-machine'
      
   print('Tag VM action! tag: "{}".'.format(tag))
   
   slackMsg = ':label: Tag VM action! tag: "' + tag + '".'
   body = {
   "channel": "#general",
   "username": "ABX",
   "text": slackMsg,
   "icon_emoji": ":bell:"
   }
   requests.post('https://hooks.slack.com/services/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', data=json.dumps(body), verify=False)
       
   return { 'tags' : tags }
