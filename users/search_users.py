'''
Copyright 2023 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Thu Feb 23 2023
File : search_users.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_user_details_by_id(baseURL, authToken, userID):
    logger.info("Entering get_user_details_by_id")

    APIOPTIONS = "?id=" + str(userID)
    userDetails = get_user_details(baseURL, authToken, APIOPTIONS)

    return userDetails

#------------------------------------------------------------------------------------------#
def get_user_details(baseURL, authToken, APIOPTIONS):
    logger.info("Entering get_user_details")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "users/search"
    RESTAPI_URL = ENDPOINT_URL + APIOPTIONS
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}   
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        logger.info("    User information retrieved")
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        raise
        
    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        return(response.json()["data"])
    else: 
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        response.raise_for_status()