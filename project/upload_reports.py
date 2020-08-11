'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Sat Aug 08 2020
File : upload_reports.py
'''

import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def upload_project_report_data(domainName, port, projectID, reportID, authToken, uploadZipflle):
    logger.info("Entering upload_project_report_data")

    RESTAPI_BASEURL = "http://" + domainName + ":" + port + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "projects/uploadReport/"
    RESTAPI_URL = ENDPOINT_URL
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    formOptions = {'projectId': str(projectID),'reportId': str(reportID)}
    files = [ ('file', open(uploadZipflle,'rb')) ]

    headers = {'Content Type': 'multipart/form-data','Authorization': 'Bearer ' + authToken}  
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.post(RESTAPI_URL, headers=headers, data=formOptions, files=files)
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error:",errh)
        return -1
        
    except requests.exceptions.ConnectionError as errc:
        logger.error("Connection Error:",errc)
        return -1

    except requests.exceptions.Timeout as errt:
        logger.error("Timeout Error:",errt)
        return -1
        
    except requests.exceptions.RequestException as err:
        logger.error("Unknown Error:",err)
        return -1 
    
    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Archive file uploaded")
        return

    elif response.status_code == 400:
        # Bad Request
        # Assume there is no task data for the project
        logger.error("Response code 400 - %s" %response.text) 
        return -1         
        
    elif response.status_code == 401:
        # Unauthorized
        logger.error("Response code 401 - %s" %response.text) 
        return -1 
        
    elif response.status_code == 404:
        # Not Found
        logger.error("Response code 404 - %s" %response.text)
        return -1 
        
    elif response.status_code == 405:
        # Method Not Allowed
        logger.error("Response code 405 - %s" %response.text)
        return -1 
        
    elif response.status_code == 500:
        logger.error("Response code 500 - %s" %response.text)
        return -1 