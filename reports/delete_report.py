'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Sun Aug 16 2020
File : delete_report.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def unregister_report(domainName, port, authToken, reportName):
    logger.info("Entering upload_project_report_data")

    RESTAPI_BASEURL = domainName + ":" + port + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "reports/"
    RESTAPI_URL = ENDPOINT_URL + reportName
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}   
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.delete(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return
        
    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        message =  response.json()["message"]
        logger.info(message)
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