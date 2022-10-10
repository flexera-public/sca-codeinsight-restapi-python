'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Mon Apr 12 2021
File : create_inventory.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def create_component_inventory_item(baseURL, projectID, componentId, componentVersionId, licenseId, authToken, inventoryItemName ):
    logger.debug("Entering create_component_inventory_item")

    component_body = '''
        {
        "projectId": "''' + str(projectID) + '''",
        "inventoryModel": {
            "name": "''' + inventoryItemName + '''",
            "inventoryType": "COMPONENT",
                "component": {
                    "id": "''' + str(componentId) + '''",
                    "versionId": "''' + str(componentVersionId) + '''",
                    "licenseId": "''' + str(licenseId) + '''"
                }
            }
        }
    ''' 

    response = create_inventory_item(baseURL, authToken, component_body)
    return response

#------------------------------------------------------------------------------------------#
def create_work_in_progress_inventory_item(baseURL, projectID, authToken, inventoryItemName ):
    logger.debug("Entering create_work_in_progress_inventory_item")

    WIP_body = '''
        {
        "projectId": "''' + projectID + '''",
        "inventoryModel": {
            "name": "''' + inventoryItemName + '''",
            "inventoryType": "WORK_IN_PROGRESS"
            }
        }
    ''' 

    response = create_inventory_item(baseURL, authToken, WIP_body)
    return response

#------------------------------------------------------------------------------------------#
def create_inventory_item(baseURL, authToken, inventoryItemBody ):
    logger.info("Entering create_inventory_item")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "inventories/"
    RESTAPI_URL = ENDPOINT_URL

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
  

    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.post(RESTAPI_URL, headers=headers, data=inventoryItemBody)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 201:
        return response.json()
    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}