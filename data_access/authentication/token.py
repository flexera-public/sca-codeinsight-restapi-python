'''
Copyright 2022 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Sat Jan 15 2022
File : token.py
'''

import logging
import requests

logger = logging.getLogger(__name__)

#---------------------------------------------------------
def generate_service_account_bearer_token(baseURL, client_id, client_secret):
    logger.info("Entering generate_service_account_bearer_token")

    RESTAPI_BASEURL = baseURL + "/oidc/token"
    RESTAPI_URL = RESTAPI_BASEURL
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)

    grant_type = "client_credentials"
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'} 

    payload = "grant_type=%s&client_id=%s&client_secret=%s" %(grant_type, client_id, client_secret)
      
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.post(RESTAPI_URL, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return
        
    
    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Bearer Token received")
        access_token = response.json()["access_token"]
        return access_token
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