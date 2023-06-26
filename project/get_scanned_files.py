'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Wed Oct 21 2020
File : get_scanned_files.py
'''
import logging
import requests

logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------------------#
def get_scanned_files_details(baseURL, projectID, authToken):
    logger.info("Entering get_scanned_files_details")
    APIOPTIONS = ""
    scannedFiles = get_scanned_files_details_with_options(baseURL, projectID, authToken, APIOPTIONS)
    return scannedFiles


#------------------------------------------------------------------------------------------#
def get_scanned_files_details_with_MD5_and_SHA1(baseURL, projectID, authToken):
    logger.info("Entering get_scanned_files_details_with_MD5_and_SHA1")

    APIOPTIONS = "&includeMD5Hash=true&includeSHA1Hash=true"

    scannedFiles = get_scanned_files_details_with_options(baseURL, projectID, authToken, APIOPTIONS)
    return scannedFiles

#------------------------------------------------------------------------------------------#
def get_scanned_files_details_with_options(baseURL, projectID, authToken, APIOPTIONS):
    logger.info("Entering get_scanned_files_details_with_options")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "projects/" + str(projectID) + "/allscannedfiles/?offset=" 
    RESTAPI_URL = ENDPOINT_URL + "1" + APIOPTIONS
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
   
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}   
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
        logger.info("    Scanned files retreived")
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        raise
        
    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:

        scannedFiles = response.json()["data"]
        currentPage = response.headers["Current-page"]
        numPages = response.headers["Number-of-pages"]
        nextPage = int(currentPage) + 1

        if int(numPages) > 1:

            # There is more than a single page of data so make an additional call to get
            # all of the data in a single call
            RESTAPI_URL = ENDPOINT_URL + "1" + "&limit=" + str(int(numPages)*25) + APIOPTIONS
            response = requests.get(RESTAPI_URL, headers=headers)
            scannedFiles = response.json()["data"]

        return scannedFiles       


    elif response.status_code == 400:

        # See if there are no results or an error
        if "Total records :0 number of pages :0" in str(response.json()["errors"]):
            logger.error("No scanned files for projects")
            return []
        else:
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