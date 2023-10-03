'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : arybak  
Created On : Tues September 15 2020
File : get_component_details.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_component_details(baseURL, componentID, authToken):
    logger.info("Entering get_component_details")
    APIOPTIONS = ""
    componentDetails = get_component_details_with_options(baseURL, componentID, authToken, APIOPTIONS)
    return componentDetails

#------------------------------------------------------------------------------------------#
def get_component_details_v3_summary(baseURL, componentID, authToken):
    logger.info("Entering get_component_details_v3_summary")
    APIOPTIONS = "vulnerabilitySummary=true&cvssVersion=V3"
    componentDetails = get_component_details_with_options(baseURL, componentID, authToken, APIOPTIONS)
    return componentDetails

#------------------------------------------------------------------------------------------#
def get_component_details_without_versions(baseURL, componentID, authToken):
    logger.info("Entering get_component_details_without_versions")
    APIOPTIONS = "includeVersions=false"
    componentDetails = get_component_details_with_options(baseURL, componentID, authToken, APIOPTIONS)
    return componentDetails

#------------------------------------------------------------------------------------------#
def get_component_details_with_options(baseURL, componentID, authToken, APIOPTIONS):
    logger.info("Entering get_component_details_with_options")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "components/"
    RESTAPI_URL = ENDPOINT_URL + str(componentID) 
    RESTAPI_URL += "?" + APIOPTIONS

    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}
   
    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Componenet details received")
        componentDetails = response.json()
        return componentDetails
    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}
