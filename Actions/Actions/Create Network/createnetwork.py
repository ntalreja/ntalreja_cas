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

def getNSXTproxy(org_id, sddc_id, sessiontoken):
    """ Gets the Reverse Proxy URL """
    myHeader = {'csp-auth-token': sessiontoken}
    myURL = "{}/vmc/api/orgs/{}/sddcs/{}".format(strProdURL,org_id, sddc_id)
    response = requests.get(myURL, headers=myHeader)
    json_response = response.json()
    proxy_url = json_response['resource_config']['nsx_api_public_endpoint_url']
    return proxy_url

def newSDDCnetworks(proxy_url, sessiontoken, display_name, gateway_address, dhcp_range, domain_name, routing_type):
    """ Creates a new SDDC Network. L2 VPN networks are not currently supported. """
    myHeader = {"Content-Type": "application/json","Accept": "application/json", 'csp-auth-token': sessiontoken}
    myURL = (proxy_url + "/policy/api/v1/infra/tier-1s/cgw/segments/" + display_name)
    # print(myURL)
    if routing_type == "DISCONNECTED" :
        json_data = {
                "subnets":[{"gateway_address":gateway_address}],
                "type":routing_type,
                "display_name":display_name,
                "advanced_config":{"connectivity":"OFF"},
                "id":display_name
                }
        print(json_data)
        response = requests.put(myURL, headers=myHeader, json=json_data)
        print(response)
        json_response_status_code = response.status_code
        if json_response_status_code == 200 :
            print("The following network has been created:")
            table = PrettyTable(['Name', 'Gateway', 'Routing Type'])
            table.add_row([display_name, gateway_address, routing_type])
            return table
        else :
            print("There was an error_1. Try again.")
            return
    else:
        if dhcp_range == "none" :
            json_data = {
                "subnets":[{"gateway_address":gateway_address}],
                "type":routing_type,
                "display_name":display_name,
                "advanced_config":{"connectivity":"ON"},
                "id":display_name
                }
            response = requests.put(myURL, headers=myHeader, json=json_data)
            json_response_status_code = response.status_code
            if json_response_status_code == 200 :
                print("The following network has been created:")
                table = PrettyTable(['Name', 'Gateway', 'Routing Type'])
                table.add_row([display_name, gateway_address, routing_type])
                return table
            else :
                print("There was an error_2. Try again.")
                return
        else :
            json_data = {
                "subnets":[{"dhcp_ranges":[dhcp_range],
                "gateway_address":gateway_address}],
                "type":routing_type,
                "display_name":display_name,
                "domain_name":domain_name,
                "advanced_config":{"connectivity":"ON"},
                "id":display_name
                }
            print(json_data)
            response = requests.put(myURL, headers=myHeader, json=json_data)
            print(response)
            json_response_status_code = response.status_code
            if json_response_status_code == 200 :
                print("The following network has been created:")
                table = PrettyTable(['Name', 'Gateway', 'DHCP', 'Domain Name', 'Routing Type'])
                table.add_row([display_name, gateway_address, dhcp_range, domain_name, routing_type])
                return table
            else :
                print("There was an error_3. Try again.")
                return
    
Refresh_Token = ""
ORG_ID = ""
SDDC_ID = ""
    
def handler(context, inputs):
    print('Create Network')
    display_name    = inputs["Name"]
    gateway_address = inputs["Gateway"]
    dhcp_range      = inputs["Range"]
    routing_type    = inputs["Type"]
    domain_name    = inputs["Domain name"]
    session_token = getAccessToken(Refresh_Token)
    proxy = getNSXTproxy(ORG_ID, SDDC_ID, session_token)
    if routing_type.lower() == "routed" and bool(dhcp_range) :
        # DHCP-Enabled Network
        routing_type = "ROUTED"
        newSDDC = newSDDCnetworks(proxy, session_token, display_name, gateway_address, dhcp_range, domain_name, routing_type)
        print(newSDDC)
    elif routing_type.lower() == "disconnected" :
        # Disconnected Network
        routing_type = "DISCONNECTED"
        dhcp_range = ""
        domain_name = ""
        newSDDC = newSDDCnetworks(proxy, session_token, display_name, gateway_address, dhcp_range, domain_name, routing_type)
        print(newSDDC)
    elif routing_type.lower() == "routed" and (bool(dhcp_range) == False) :
        # Static Network
        dhcp_range = "none"
        domain_name = ""
        routing_type = "ROUTED"
        newSDDC = newSDDCnetworks(proxy, session_token, display_name, gateway_address, dhcp_range, domain_name, routing_type)
        print(newSDDC)
    else:
        print("Incorrect syntax. Try again or check the help.")