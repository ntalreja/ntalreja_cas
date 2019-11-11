def handler(context,inputs):
    #update a static BP property MyProp with inherited project property for use in blueprint expression
    
    outputs = {}
    outputs['customProperties'] = inputs['customProperties']
    outputs['customProperties']['myproperty'] = inputs['customProperties']['anyproperty']
    
    return outputs
