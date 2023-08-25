'''
Copyright 2022 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Sat Jan 15 2022
File : license_texts.py
'''


import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_license_text_by_licenseTextId(baseURL, authToken, licenseTextId):
    logger.info("Entering get_license_text_by_licenseTextId")

    APIVersion = "v1"

    RESTAPI_BASEURL = baseURL + "/sdl"
    ENDPOINT_URL = RESTAPI_BASEURL + "/" + APIVersion + "/licensetexts"
    RESTAPI_URL = ENDPOINT_URL + "/" + licenseTextId
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Authorization': 'Bearer ' + authToken}   
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        raise
        
    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        licenseText = response.json()
        return licenseText
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

#------------------------------------------------------------------------------------------#
def get_license_text_by_componentVersionId(baseURL, authToken, componentVersionIds):
    logger.info("Entering get_license_text_by_componentVersionId")

    APIVersion = "v1"

    RESTAPI_BASEURL = baseURL + "/sdl"
    ENDPOINT_URL = RESTAPI_BASEURL + "/" + APIVersion + "/licensetexts"
    RESTAPI_URL = ENDPOINT_URL + "?versionIds=" + componentVersionIds
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Authorization': 'Bearer ' + authToken}   
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        raise
        
    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        licenseText = response.json()
        return licenseText["data"]
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
