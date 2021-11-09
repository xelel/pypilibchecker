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
    releases = list(data['releases'].keys())
    latest_version = releases[-1]
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

#list with libs versions info
list_libs_info_versions=[]
for package in libs_list:

    if package.find('==') > 0:
        index = package.find('==')
        package_name = package[0:index]
        current_version = package[index + 2::]
        dict_lib_info=pypi_api_request(package_name, current_version)
        list_libs_info_versions.append(dict_lib_info)

    elif package.find('>=') > 0:
        index = package.find('>=')
        package_name = package[0:index]
        current_version= package[index + 2::]
        dict_lib_info=pypi_api_request(package_name,current_version)
        list_libs_info_versions.append(dict_lib_info)

    elif package.find('[') > 0:
        index = package.find('[')
        package_name = package[0:index]
        dict_lib_info=pypi_api_request(package_name)
        list_libs_info_versions.append(dict_lib_info)
    else:
        package_name = package
        dict_lib_info=pypi_api_request(package_name)
        list_libs_info_versions.append(dict_lib_info)
pp.pprint(list_libs_info_versions)

json_object = json.dumps(list_libs_info_versions,indent=4)
with open("libs_version_info.json", "w") as outfile:
    outfile.write(json_object)