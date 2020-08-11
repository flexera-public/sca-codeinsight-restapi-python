'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Sun Aug 07 2020
File : get_project_inventory.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_project_inventory_details(domainName, port, projectID, authToken):
    logger.info("Entering get_project_inventory")

    RESTAPI_BASEURL = "http://" + domainName + ":" + port + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "project/inventory/"
    
    RESTAPI_URL = ENDPOINT_URL + str(projectID) + "?published=true" 
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error:",errh)
        return -1
        
    except requests.exceptions.ConnectionError as errc:
        logger.error("Connection Error:",errc)
        return -1

    except requests.exceptions.Timeout as errt:
        logger.error("Timeout Error:",errt)
        return -1
        
    except requests.exceptions.RequestException as err:
        logger.error("Unknown Error:",err)
        return -1 
    
    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Project inventory received")
        INVENTORY = (response.json())
        return INVENTORY

    elif response.status_code == 400:
        # Bad Request
        # Assume there is no task data for the project
        logger.error("Response code 400 - %s" %response.text) 
        return -1         
        
    elif response.status_code == 401:
        # Unauthorized
        logger.error("Response code 401 - %s" %response.text) 
        return -1 
        
    elif response.status_code == 404:
        # Not Found
        logger.error("Response code 404 - %s" %response.text)
        return -1 
        
    elif response.status_code == 405:
        # Method Not Allowed
        logger.error("Response code 405 - %s" %response.text)
        return -1 
        
    elif response.status_code == 500:
        logger.error("Response code 500 - %s" %response.text)
        return -1 