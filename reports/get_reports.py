'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Sun Aug 16 2020
File : get_reports.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_currently_registered_reports(domainName, port, authToken):
    logger.info("Entering upload_project_report_data")

    RESTAPI_BASEURL = "http://" + domainName + ":" + port + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "reports/"
    RESTAPI_URL = ENDPOINT_URL
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}   
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        logger.info("    Current report list retreived")
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return
        
    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        return(response.json()["data"])
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