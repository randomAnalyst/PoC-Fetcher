import requests
import re
import json

def cve_to_poc(cve_ids):
    final_dict = {}
    for cve in cve_ids:
        poc_list = []

        try:
            year = re.findall("-(\d{4})-",cve)[0]
        except:
            print("Error while parsing cve : ",cve)
            continue

        #fetching data from nomi-sec
        url = f"https://raw.githubusercontent.com/nomi-sec/PoC-in-GitHub/master/{year}/{cve}.json"
        response = requests.get(url)
        if(response.status_code == 404):
            final_dict[cve] = []
            continue
        response_string = str(response.content,"utf-8")
        #extracting the POC url
        poc_data = json.loads(response_string)
        for poc in poc_data:
            poc_list.append(poc["html_url"])
        #final dict for cve-poc data 
        final_dict[cve] = poc_list

    return final_dict

#Accepting comma separated CVEs
cve_ids = input("Enter the CVEids : ").upper()
cve_ids = cve_ids.split(",")

#fetching POCs
poc_dict = cve_to_poc(cve_ids)

#printing the POC list
for cve,poc_list in poc_dict.items():
    print(cve," : ")
    if(poc_list == []):
        print("\t No POCs found")
    for poc in poc_list:
        print("\t",poc)
