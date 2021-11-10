import json
from packaging import version
import requests
import re
import pprint as pp

def pypi_api_request(package_name,current_version=None):

    """
        Pypi API query and check package version.

    Args:
    package_name (str): package name to be verified

    current_version(str): current package version

    Returns:
    lib_dict_info (dict): dict with the package versions informations
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    r = requests.get(url)
    data = r.json()
    latest_version = data['info']['version']
    libs_list = re.findall(r'\w.+', requirements_file_text)
    outofDate=''

    if current_version==None:
        current_version=latest_version
        outofDate=False

    elif version.parse(latest_version)==version.parse(current_version):
        outofDate=False

    elif version.parse(latest_version)!=version.parse(current_version):
        outofDate=True

    dict_lib_info={"packageName": package_name,
        "currentVersion": current_version,
        "latestVersion": latest_version,
            "outOfDate": outofDate}

    return dict_lib_info


#open requirements file
with open('requirements.txt') as f:
    requirements_file_text = f.read()

#create lib list with regex
libs_list = re.findall(r'\w.+', requirements_file_text)

requirements_list_info=[]

for lib in libs_list:
    
    if '==' in lib:
        lib_name=re.findall(r'(\w+)=',lib)
        lib_name=lib_name[0]
        lib_version=re.findall(r'=([0-9.]+)',lib)
        lib_version=lib_version[0]
        lib_info=pypi_api_request(lib_name,lib_version)
        requirements_list_info.append(lib_info)
    
    elif '>' in lib:
        lib_name=re.findall(r'(\w+)>',lib)
        lib_name=lib_name[0]
        lib_version=re.findall(r'=([0-9.]+)',lib)
        lib_version=lib_version[0]
        lib_info = pypi_api_request(lib_name, lib_version)
        requirements_list_info.append(lib_info)
    
    elif '~=' in lib:
        lib_name=re.findall(r'(\w+)~',lib)
        lib_name=lib_name[0]
        lib_version=re.findall(r'=([0-9.]+)',lib)
        lib_version=lib_version[0]
        lib_info = pypi_api_request(lib_name, lib_version)
        requirements_list_info.append(lib_info)
    
    elif '[' and ']' in lib:
        lib_name=re.findall(r'(\w+)\[\w+]',lib)
        lib_name=lib_name[0]
        lib_info=pypi_api_request(lib_name,None)
        requirements_list_info.append(lib_info)
    
    else:
        lib_name=lib
        lib_info = pypi_api_request(lib_name, None)
        requirements_list_info.append(lib_info)

json_object = json.dumps(requirements_list_info,indent=4)
with open("libs_version_info.json", "w") as outfile:
    outfile.write(json_object)