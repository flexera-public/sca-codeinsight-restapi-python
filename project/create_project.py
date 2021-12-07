'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Fri Dec 03 2021
File : create_project.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def create_project(baseURL, authToken, projectName, projectOptions):
    logger.info("Entering create_project_folder")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "projects/"
    RESTAPI_URL = ENDPOINT_URL

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
    
    body = '''{ "name": "''' + projectName + '''"'''

    # Add each optoin to override any defaults that need to be changed
    for option in projectOptions:
        body += ","
        body += '''"''' + option + '''" : "''' + projectOptions[option] + '''"'''
            
    body += '''}'''

    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.post(RESTAPI_URL, headers=headers, data=body)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)


    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 201:
        projectID = response.json()["id"]
        logger.debug("        Project created with ID: %s" %projectID)
        return projectID
    elif response.status_code == 400:
        # Is this an error we can handle?
        errorMessage = response.json()["errors"][0]["message"]
        if errorMessage.endswith("already exists."):
            logger.debug("        Project already exists.  Get existing ID")
            return errorMessage
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