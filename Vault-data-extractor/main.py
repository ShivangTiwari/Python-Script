import hvac
import requests
import csv 
from Functions import get_keys
from Functions import get_data
from Functions import get_version_no
# Authenticate with Vault using hvac
vault_url = 'https://vault.uat-hdfclz.zetapay.in/'
vault_token = 'hvs.CAESICgYaBKK-o7SvyZvE0lR0tYSZMoV0RySv7rOzIOGwxPOGh4KHGh2cy5BNERFSmlkOVNEd3poZXltbmlPMTRBTVE'
headers = {
    "X-Vault-Token": vault_token
}

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

                        # print(list_key)
                            
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
