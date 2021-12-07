'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Fri Dec 03 2021
File : upload_project_codebase.py
'''

import logging
import requests

logger = logging.getLogger(__name__)

#--------------------------------------------------
def upload_archive(projectID, zipFileContents, baseURL, authToken):

    apiOptions = "&deleteExistingFileOnServer=true&expansionLevel=1" 

    apiEndPoint = baseURL + "/codeinsight/api/project/uploadProjectCodebase"
    apiEndPoint += "?projectId=" + str(projectID) + apiOptions
  
    logger.debug("    apiEndPoint: %s" %apiEndPoint)
    headers = {'Content-Type': 'application/octet-stream', 'Authorization': 'Bearer ' + authToken}  
    
    #  Make the request to get the required data   
    try:
        response = requests.post(apiEndPoint, headers=headers, data=zipFileContents)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        if  "File upload successful" in response.json()["Content: "]:
            logger.debug("File uploaded")
    else:
        logger.error(response.text)
        return 