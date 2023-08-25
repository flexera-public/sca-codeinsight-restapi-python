'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Tue Dec 07 2021
File : generate_report.py
'''

import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def generate_report(projectID,  reportID, reportOptions, codeInsightURL, authToken):
    logger.debug("Entering generate_report")

    apiEndPoint = codeInsightURL + "/codeinsight/api/projects"
    apiEndPoint += "/" + str(projectID)
    apiEndPoint += "/reports/" + str(reportID)
    apiEndPoint += "/generate"
  
    logger.debug("    apiEndPoint: %s" %apiEndPoint)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
    
    #  Make the request to get the required data   
    try:
        response = requests.post(apiEndPoint, headers=headers, data=reportOptions)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        taskID = response.json()["data"]["taskId"]
        logger.debug("Report generated with task ID: %s" %taskID)
        return taskID
    else:
        logger.error(response.text)
        return 
