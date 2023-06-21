'''
Copyright 2023 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Wed Jun 21 2023
File : get_inventory_history.py
'''
import logging
import requests
logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------------------#
def get_inventory_history_details(baseURL, inventoryID, authToken):
    
    logger.info("Entering get_inventory_history_details")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "inventories/" + str(inventoryID) + "/history?offset=" 
    RESTAPI_URL = ENDPOINT_URL + "1"
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
        logger.info("    Project inventory history received")
        projectInventoryHistory = response.json()["data"]
        currentPage = response.headers["Current-page"]
        numPages = response.headers["Number-of-pages"]
        nextPage = int(currentPage) + 1

        while int(nextPage) <= int(numPages):
            RESTAPI_URL = ENDPOINT_URL + str(nextPage)
            logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
            response = requests.get(RESTAPI_URL, headers=headers)

            nextPage = int(response.headers["Current-page"]) + 1
            projectInventoryHistory.update(response.json()["data"])

        return projectInventoryHistory

    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}