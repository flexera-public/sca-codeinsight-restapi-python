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
        return
        
    
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

    elif response.status_code == 400:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Bad Request" %response.status_code )
        response.raise_for_status()
    elif response.status_code == 401:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Unauthorized" %response.status_code )
        response.raise_for_status() 
    elif response.status_code == 404:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Not Found" %response.status_code )
        response.raise_for_status()   
    else: 
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        response.raise_for_status()

#------------------------------------------------------------------------------------------#
def get_project_inventory_details_without_vulnerabilities(baseURL, projectID, authToken):
    logger.info("Entering get_project_inventory_details_without_vulnerabilities")

    APIOPTIONS = "&skipVulnerabilities=true"
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
        return
        
    
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

    elif response.status_code == 400:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Bad Request" %response.status_code )
        response.raise_for_status()
    elif response.status_code == 401:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Unauthorized" %response.status_code )
        response.raise_for_status() 
    elif response.status_code == 404:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Not Found" %response.status_code )
        response.raise_for_status()   
    else: 
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        response.raise_for_status()