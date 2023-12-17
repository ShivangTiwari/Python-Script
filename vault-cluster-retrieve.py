import hvac
import requests
import csv 
from tabulate import tabulate

# Authenticate with Vault using hvac
vault_url = 'https://vault.uat-hdfclz.zetapay.in/'

vault_token = #put vault token here

headers = {
    "X-Vault-Token": vault_token
}

def get_data(vault_resource_url, vault_token):
    # Making GET request to the Vault resource using requests
    keys=[]
    response = requests.get(vault_resource_url, headers={'X-Vault-Token': vault_token})
    # print("response---->",response, "its usrl is ", vault_resource_url)
    if response.status_code == 200:
        data= response.json()
        keys = data.get('data', {}).get('keys', [])
        return keys
    else:
        return keys

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

def validateIfToken(v):
    if(type(v)==str):
        return len(v) >= 256

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
        for key, value in data_items_list:
            v=validateIfToken(value)
            if(v):
                list_key.append(key)
    else:
        print(f"Request failed with status code {response.status_code}")


try:
    with open('testing.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Cluster Name", "Service Name", "multi-cluster","TenantValue", "Tenant value", "Application","keys"])

        vault_resource_url = f'{vault_url}/v1/secrets/metadata/cluster/?list=true'
        # print("going for first iteration")
        keys=get_data(vault_resource_url,vault_token)
        for i in range(0,len(keys)):
            vault_resource_url = f'{vault_url}/v1/secrets/metadata/cluster/{keys[i]}/?list=true'
            keys2=get_data(vault_resource_url,vault_token)
            
            for j in range(0,len(keys2)):
                # print("loop2")
                vault_resource_url = f'{vault_url}/v1/secrets/metadata/cluster/{keys[i]}/{keys2[j]}/?list=true'
                keys3=get_data(vault_resource_url,vault_token)
                # print(keys[i],keys2[j],keys3)
                if "tenants/" in keys3 or "application" in keys3 or "application.properties" in keys3:
                    key4=[]
                    list_key=[]
                    if "tenants/" in keys3:
                        vault_resource_url = f'{vault_url}/v1/secrets/metadata/cluster/{keys[i]}/{keys2[j]}/tenants/?list=true'
                        keys4=get_data(vault_resource_url,vault_token)

                    if "application" in keys3:
                        vault_resource_url = f'{vault_url}/v1/secrets/metadata/cluster/{keys[i]}/{keys2[j]}/application'
                        version_no=get_version_no(vault_resource_url,headers)
                        variable='?version='
                        vault_resource_urll=f'{vault_url}/v1/secrets/data/cluster/{keys[i]}/{keys2[j]}/application{variable}{version_no}'
                        
                        get_keys(vault_resource_urll,headers,list_key)

                    if "application.properties" in keys3:
                        vault_resource_url = f'{vault_url}/v1/secrets/metadata/cluster/{keys[i]}/{keys2[j]}/application.properties'
                        version_no=get_version_no(vault_resource_url,headers)
                        variable='?version='
                        vault_resource_urll=f'{vault_url}/v1/secrets/data/cluster/{keys[i]}/{keys2[j]}/application.properties{variable}{version_no}'
                        
                        get_keys(vault_resource_urll,headers,list_key)

                    if "tenants/" in keys3:
                        if "application" in keys3:
                            csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),"NO-multi-cluster","tenant",keys4,"Application",list_key]) 
                        elif "application.properties" in keys3:
                            csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),"NO-multi-cluster","tenant",keys4,"Application properties",list_key]) 
                        else:
                            csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),"NO-multi-cluster","tenant",keys4,"Application","Not found"]) 

                    else:
                        if "application" not in keys3 and "application.properties" not in keys3:
                            csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),"NO-multi-cluster","tenant","tenant not found","Application", "application/application.properties not found"]) 
                        elif "application" in keys3:
                            csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),"NO-multi-cluster","tenant","tenant not found","Application",list_key]) 
                        elif "application.properties" in keys3:
                            csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),"NO-multi-cluster","tenant","tenant not found","Application properties",list_key]) 

                else:

                    for k in range(0,len(keys3)):
                        vault_resource_url = f'{vault_url}/v1/secrets/metadata/cluster/{keys[i]}/{keys2[j]}/{keys3[k]}/?list=true'
                        keys4=get_data(vault_resource_url,vault_token)
                        
                        keys5=[]
                        list_key=[]
                        if "tenants/" in keys4:
                            vault_resource_url = f'{vault_url}/v1/secrets/metadata/cluster/{keys[i]}/{keys2[j]}/{keys3[k]}/tenants/?list=true'
                            keys5=get_data(vault_resource_url,vault_token)

                        if "application" in keys4:
                            vault_resource_url = f'{vault_url}/v1/secrets/metadata/cluster/{keys[i]}/{keys2[j]}/{keys3[k]}/application'
                            version_no=get_version_no(vault_resource_url,headers)
                            variable='?version='
                            vault_resource_urll=f'{vault_url}/v1/secrets/data/cluster/{keys[i]}/{keys2[j]}/{keys3[k]}/application{variable}{version_no}'
                            get_keys(vault_resource_urll,headers,list_key)


                        if "application.properties" in keys4:
                            vault_resource_url = f'{vault_url}/v1/secrets/metadata/cluster/{keys[i]}/{keys2[j]}/{keys3[k]}/application.properties'
                            version_no=get_version_no(vault_resource_url,headers)
                            variable='?version='
                            vault_resource_urll=f'{vault_url}/v1/secrets/data/cluster/{keys[i]}/{keys2[j]}/{keys3[k]}/application.properties{variable}{version_no}'
                            get_keys(vault_resource_urll,headers,list_key)

                        print(list_key)
                            
                        if "tenants/" in keys4:
                            if "application" in keys4:
                                csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),keys3[k].replace("/", ""),"tenant",keys5,"Application",list_key]) 
                            elif "application.properties" in keys4:
                                csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),keys3[k].replace("/", ""),"tenant",keys5,"Application properties",list_key]) 
                        else:
                            if "application" not in keys4 and "application.properties" not in keys4:
                                csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),keys3[k].replace("/", ""),"tenant","tenant not found","Application", "application not found"]) 
                            elif "application" in keys4:
                                csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),keys3[k].replace("/", ""),"tenant","tenant not found","Application",list_key]) 
                            elif "application.properties" in keys4:
                                csv_writer.writerow([keys[i].replace("/", ""),keys2[j].replace("/", ""),keys3[k].replace("/", ""),"tenant","tenant not found","Application properties",list_key]) 

                
                



except Exception as e:
    print(f'Error: {str(e)}')
