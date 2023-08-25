'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Sun Aug 16 2020
File : get_project_inventory.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_project_inventory_details(baseURL, projectID, authToken):
    logger.info("Entering get_project_inventory")
    APIOPTIONS = ""
    projectInventory = get_project_inventory_details_with_options(baseURL, projectID, authToken, APIOPTIONS)
    return projectInventory

#------------------------------------------------------------------------------------------#
def get_project_inventory_details_without_files_or_vulnerabilities(baseURL, projectID, authToken):
    logger.info("Entering get_project_inventory_details_without_files_or_vulnerabilities")
    APIOPTIONS = "&includeFiles=false&skipVulnerabilities=true"
    projectInventory = get_project_inventory_details_with_options(baseURL, projectID, authToken, APIOPTIONS)
    return projectInventory


#------------------------------------------------------------------------------------------#
def get_project_inventory_details_without_files(baseURL, projectID, authToken):
    logger.info("Entering get_project_inventory_details_without_files")
    APIOPTIONS = "&includeFiles=false"
    projectInventory = get_project_inventory_details_with_options(baseURL, projectID, authToken, APIOPTIONS)
    return projectInventory

#------------------------------------------------------------------------------------------#
def get_unpublished_project_inventory_details_without_vulnerabilities(baseURL, projectID, authToken):
    logger.info("Entering get_project_inventory_details_without_vulnerabilities")
    APIOPTIONS = "&skipVulnerabilities=true&published=false"
    projectInventory = get_project_inventory_details_with_options(baseURL, projectID, authToken, APIOPTIONS)
    return projectInventory


#------------------------------------------------------------------------------------------#
def get_project_inventory_details_without_vulnerabilities(baseURL, projectID, authToken):
    logger.info("Entering get_project_inventory_details_without_vulnerabilities")
    APIOPTIONS = "&skipVulnerabilities=true"
    projectInventory = get_project_inventory_details_with_options(baseURL, projectID, authToken, APIOPTIONS)
    return projectInventory

#------------------------------------------------------------------------------------------#
def get_project_inventory_details_with_options(baseURL, projectID, authToken, APIOPTIONS):
    logger.info("Entering get_project_inventory_details_with_options")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "project/inventory/" + str(projectID) + "?page=" 
    RESTAPI_URL = ENDPOINT_URL + "1" + APIOPTIONS
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}
        
    
    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Project inventory received")
        projectInventory = response.json()
        currentPage = response.headers["Current-page"]
        numPages = response.headers["Number-of-pages"]
        nextPage = int(currentPage) + 1

        while int(nextPage) <= int(numPages):
            RESTAPI_URL = ENDPOINT_URL + str(nextPage) + APIOPTIONS
            logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
            response = requests.get(RESTAPI_URL, headers=headers)

            nextPage = int(response.headers["Current-page"]) + 1
            projectInventory["inventoryItems"] += response.json()["inventoryItems"] 

        return projectInventory

    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}
 