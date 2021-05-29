'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Fri May 28 2021
File : update_report.py
'''

import logging
import requests
import json

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def update_custom_report(reportName, reportPath, reportID, reportOrder, enableProjectPickerValue, reportOptions, baseURL, authToken):
    logger.info("Entering update_custom_report")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "reports/"
    RESTAPI_URL = ENDPOINT_URL
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)

    #Take the list of reportOptions and create a string
    if len(reportOptions):
        optionsString = ""
        for option in reportOptions:
            optionsString += json.dumps(option) +","

        optionsString = optionsString[:-1]

    else:
        optionsString = ""


    createReportBody = '''
    {
        "id" : "''' + str(reportID) + '''",
        "name": "''' + reportName + '''",
        "path": "''' + reportPath + '''",
        "order": "''' + str(reportOrder) + '''",
        "enabled": "true",
        "enableProjectPicker": "''' + enableProjectPickerValue + '''",
        "reportOptions" : [''' + optionsString + ''']
    }'''
   
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}     
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.put(RESTAPI_URL, headers=headers, data=createReportBody)
        logger.info("    Current report list retreived")
    except requests.exceptions.RequestException as error:  # Just catch all errors
        print(response)
        logger.error(error)
        #return

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.debug("%s was sucessfully updated" %(reportName))
        return

    elif response.status_code == 400:
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