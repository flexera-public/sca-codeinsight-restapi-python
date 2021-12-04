'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Fri Dec 03 2021
File : get_project_id.py
'''
import logging
import requests
logger = logging.getLogger(__name__)

def get_projectID(baseURL, authToken, projectName):

    logger.info("Entering def get_projectID")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "projects/"
    RESTAPI_URL = ENDPOINT_URL

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 


    apiEndPoint = baseURL + "/codeinsight/api/project/id"
    apiEndPoint += "/?projectName=" + projectName
  
    logger.debug("    apiEndPoint: %s" %apiEndPoint)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
    
    #  Make the request to get the required data   
    try:
        response = requests.get(apiEndPoint, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        projectID = response.json()["Content: "]
        logger.debug("%s has a corresponding project ID of: %s" %(projectName, projectID))
        return projectID
    else:
        logger.error(response.text)
        return 