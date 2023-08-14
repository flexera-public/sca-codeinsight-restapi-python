'''
Copyright 2023 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Sun Aug 13 2023
File : release.py
'''
import logging, requests, json

logger = logging.getLogger(__name__)
#----------------------------------------------------
def get_release_details(baseURL, authToken):
    logger.debug("Entering get_release_details.")

    RESTAPI_BASEURL = "%s/codeinsight/api" %(baseURL)
    RESTAPI_URL = "%s/v1/agent/supports" %(RESTAPI_BASEURL)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}   

    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        return {"error" : error}

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        releaseDetails = json.loads(response.json()["Content: "])
        return releaseDetails
    else:
        return {"error" : response.text}