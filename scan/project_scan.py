'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Mon Dec 06 2021
File : project_scan.py
'''
import logging
import requests

logger = logging.getLogger(__name__)


#--------------------------------------------------
def scan_project(projectID, codeInsightURL, authToken):

    apiEndPoint = codeInsightURL + "/codeinsight/api/scanResource/projectScan"
    apiEndPoint += "/" + str(projectID)
  
    logger.debug("    apiEndPoint: %s" %apiEndPoint)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
    
    #  Make the request to get the required data   
    try:
        response = requests.post(apiEndPoint, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        scanID = response.json()["Content: "]
        logger.debug("Scan started with ID: %s" %scanID)
        return scanID
    else:
        logger.error(response.text)
        return 
