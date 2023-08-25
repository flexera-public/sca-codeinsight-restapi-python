'''
Copyright 2023 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Fri Aug 25 2023
File : update_notices.py
'''

import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def update_project_notices(baseURL, authToken, projectID):
    logger.debug("Entering update_project_notices")

    apiEndPoint = baseURL + "/codeinsight/api/jobs"
    apiEndPoint += "/notices/" + str(projectID)
    apiEndPoint += "?overwrite=true"
  
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
    if response.status_code == 202:
        logger.debug("Notices being fetched for project : %s" %projectID)
        return response.json()
    else:
        logger.error(response.text)
        return 
