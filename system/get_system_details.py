'''
Copyright 2023 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Sun Mar 12 2023
File : get_system_details.py
'''
import logging
import requests

logger = logging.getLogger(__name__)
#----------------------------------------------------
def get_release_information(baseURL):

    RESTAPI_BASEURL = "%s/codeinsight" %(baseURL)
    RESTAPI_URL = "%s/springmvc/contextData" %(RESTAPI_BASEURL)

    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        return {"error" : error}


    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:

        # Parse the response to create a dict response
        releaseInformation = response.text.split('version-info')[1][2:].split('</div>')[0]

        if "Revenera SCA" in releaseInformation:
            releaseInformation = releaseInformation.split()
            releaseYear = releaseInformation[5]
            releaseVersion = releaseInformation[6]

        else:
            releaseInformation = releaseInformation.split(" ", 4)
            releaseYear = releaseInformation[2]
            releaseVersion = releaseInformation[3]
   
        releaseDetails = {}
        releaseDetails["releaseYear"] = releaseYear
        releaseDetails["releaseVersion"] = releaseVersion
        releaseDetails["vendor"] = "Revenera"
        releaseDetails["tool"] = "Revenera SCA - Code Insight"

        return releaseDetails

    else:
        return {"error" : response.text}