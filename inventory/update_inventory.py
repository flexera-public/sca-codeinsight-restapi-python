'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Tue Dec 28 2021
File : update_inventory.py
'''

import logging
import requests
import re

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def update_inventory_notices_text(inventoryID, noticesText, baseURL, authToken):
    logger.info("Entering update_inventory_notices_text")

    # Escape some special characters
    noticesText = noticesText.replace(r'"', '\\"')
    noticesText = noticesText.replace("\n", "\\n")
    noticesText = noticesText.replace("\t", "\\t")
    noticesText = noticesText.replace("\r", "\\r")
    noticesText = noticesText.replace("\f", "\\f")

    updateBody = ''' { "noticeText" : "''' + noticesText + '''" }'''

    if update_inventory_item_details(inventoryID, updateBody, baseURL, authToken ):
        logger.info("Inventory Notices updated")
        return True
    else:
        logger.error("Error updating inventory notices field")
        return False


#------------------------------------------------------------------------------------------#
def update_inventory_item_details(inventoryID, updateBody, baseURL, authToken ):
    logger.info("Entering update_inventory_item_details")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "inventories/"
    RESTAPI_URL = ENDPOINT_URL + str(inventoryID)

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 


    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.put(RESTAPI_URL, headers=headers, data=updateBody.encode('utf-8'))
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)


    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("Inventory item updated")
        return True
    elif response.status_code == 400:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Bad Request" %response.status_code )
        response.raise_for_status()
    elif response.status_code == 401:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Unauthorized" %response.status_code )
        response.raise_for_status()    
    else: 
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        response.raise_for_status()