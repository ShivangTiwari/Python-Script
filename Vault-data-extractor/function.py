
import requests

def get_keys(vault_resource_url,headers,list_key):
    response = requests.get(vault_resource_url, headers=headers)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        # Extract key-value pairs from the "data" field
        data = response_data.get("data", {})
        data_items = data['data'].items()
        data_items_list = list(data_items)
        print("get_keys",data_items_list)
        for key, value in data_items_list:
            v=validateIfToken(value)
            if(v):
                list_key.append(key)
    else:
        print(f"Request failed with status code {response.status_code}")

def validateIfToken(v):
    if(type(v)==str):
        return len(v) >= 256
    
def get_version_no(vault_resource_url,headers):
    response = requests.get(vault_resource_url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        current_version = response_json.get("data", {}).get("current_version")
        if current_version is not None:
            return current_version
        else:
            print("Current Version not found in the response.")
    else:
        print(f"Request failed with status code {response.status_code}")

def get_data(vault_resource_url, vault_token):
    # Making GET request to the Vault resource using requests
    keys=[]
    response = requests.get(vault_resource_url, headers={'X-Vault-Token': vault_token})
    # print("response---->",response, "its usrl is ", vault_resource_url)
    if response.status_code == 200:
        data= response.json()
        keys = data.get('data', {}).get('keys', [])
        print("get data", keys)
        return keys
    else:
        return keys

def get_keys2(vault_resource_url,headers):
    list_key=[]
    response = requests.get(vault_resource_url, headers=headers)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        # Extract key-value pairs from the "data" field
        data = response_data.get("data", {})
        data_items = data['data'].items()
        data_items_list = list(data_items)
        for key, value in data_items_list:
            if "rds.amazonaws.com" in str(value):
                list_key.append(key)
                list_key.append(value)
                return list_key
            # if key=="SPRING_DATASOURCE_URL":
            #     return value
    else:
        print(f"Request failed with status code {response.status_code}")
