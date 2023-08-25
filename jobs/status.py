'''
Copyright 2023 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Fri Aug 25 2023
File : status.py
'''
'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Mon Dec 06 2021
File : scan_status.py
'''
import logging
import requests

logger = logging.getLogger(__name__)
#--------------------------------------------------
def get_job_status(jobID, codeInsightURL, authToken):

    apiEndPoint = codeInsightURL + "/codeinsight/api/jobs"
    apiEndPoint += "/" + str(jobID)
  
    logger.debug("    apiEndPoint: %s" %apiEndPoint)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
    
    #  Make the request to get the required data   
    try:
        response = requests.get(apiEndPoint, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        job_status = response.json()

        return job_status
    else:
        logger.error(response.text)
        return 
