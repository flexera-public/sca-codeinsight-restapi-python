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

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def update_technopedia_id(inventoryID, customFieldId, technopediaId, baseURL, authToken):
    logger.info("Entering update_inventory_notices_text")

    updateBody = '''{ 
                        "customFields": [
                            {
                                "id": "''' + str(customFieldId) + '''",
                                "value": "''' + technopediaId + '''"
                            }
                        ]
                    }'''

    response =  update_inventory_item_details(inventoryID, updateBody, baseURL, authToken )
    return response


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

    response =  update_inventory_item_details(inventoryID, updateBody, baseURL, authToken )
    return response


#------------------------------------------------------------------------------------------#
def update_inventory_item_details(inventoryID, updateBody, baseURL, authToken ):
    logger.info("    Entering update_inventory_item_details")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "inventories/"
    RESTAPI_URL = ENDPOINT_URL + str(inventoryID)

    logger.debug("        RESTAPI_URL: %s" %RESTAPI_URL)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 

    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.put(RESTAPI_URL, headers=headers, data=updateBody.encode('utf-8'))
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}

    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Inventory item deleted.")
        return response.json()
    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}
