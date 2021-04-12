'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Tue Apr 06 2021
File : add_files_to_inventory.py
'''

import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def add_files_to_inventory_and_mark_as_reviewed(baseURL, inventoryID, authToken, filePaths):
    logger.info("Entering add_files_to_inventory_and_mark_as_reviewed")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "inventories/"
    RESTAPI_URL = ENDPOINT_URL + str(inventoryID) + "/files"

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 

    filePathString = '''"'''

    for filePath in filePaths:
        filePathString += filePath + '''", "'''

    # Get rid of the last final comma, space and quote
    filePathString = filePathString[:-3]
    
    body = '''
        {
        "filePaths": [''' + filePathString + '''],
        "markAssociatedFilesAsReviewed": "true"
        }
    ''' 
       
    logger.debug(body)

    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.put(RESTAPI_URL, headers=headers, data=body)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)


    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.debug("Files were sucessfully added to the inventory item")
        return
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