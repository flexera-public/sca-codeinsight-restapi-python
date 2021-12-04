'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Wed Sep 22 2021
File : search_tasks.py
'''

import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_all_tasks_for_project(baseURL, authToken, projectID):
    logger.info("Entering get_all_tasks_for_project")

    APIOPTIONS = "?projectId=" + str(projectID)
    currentTasks = get_all_tasks(baseURL, authToken, APIOPTIONS)

    return currentTasks



#------------------------------------------------------------------------------------------#
def get_all_tasks(baseURL, authToken, APIOPTIONS):
    logger.info("Entering get_all_tasks")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "tasks/search"
    RESTAPI_URL = ENDPOINT_URL + APIOPTIONS
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}   
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        logger.info("    Current tasks retreived")
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        raise
        
    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        return(response.json()["data"])
    elif response.status_code == 400:
        # Are there just no tasks?
        if (response.json()["errors"][0]["message"]) == "The page 1 you requested is out of bounds. Total records :0 number of pages :0":
            return []  # Just return an empty list
        else:
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