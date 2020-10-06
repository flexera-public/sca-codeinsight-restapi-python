'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Tue Oct 06 2020
File : get_child_projects.py
'''

import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_child_projects_recursively(baseURL, projectID, authToken):
    logger.info("Entering upload_project_report_data")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "projects/"
    RESTAPI_URL = ENDPOINT_URL + projectID + "/childProjects?recursive=true"
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}  
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Child project listing received")
        childProjects = response.json()["data"]
        return childProjects
    elif response.status_code == 400:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Bad Request" %response.status_code )
        response.raise_for_status()
    elif response.status_code == 401:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Unauthorized" %response.status_code )
        response.raise_for_status()   
    elif response.status_code == 404:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Not Found" %response.status_code )
        response.raise_for_status()   
    else: 
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        response.raise_for_status()