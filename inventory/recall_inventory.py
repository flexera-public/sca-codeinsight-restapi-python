'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Mon Apr 26 2021
File : recall_inventory.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def recall_inventory_item(baseURL, inventoryID, authToken):
    logger.info("Entering recall_inventory_item")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "inventories/"
    RESTAPI_URL = ENDPOINT_URL + str(inventoryID) + "/recall"
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.put(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        return response.json()
    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}