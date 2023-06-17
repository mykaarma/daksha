"""
Daksha
Copyright (C) 2021 myKaarma.
opensource@mykaarma.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import json
import os
from concurrent.futures.thread import ThreadPoolExecutor

from django.http import HttpResponse,JsonResponse
from rest_framework import status

from daksha.settings import REPO_NAME, BRANCH_NAME, TEST_RESULT_DB
from .errors import UnsupportedFileSourceError, BadArgumentsError
from .testreport_generator import *
from .thread_executor import thread_executor
from .utils.utils import read_yaml, read_local_yaml, get_yml_files_in_folder_local, get_yml_files_in_folder_git
from .models import TestResults,GetTestResults


# Create your views here.
def executor(request):
    """
    Receives http request and starts execution of Test

    """
    if request.method == 'POST':
        try:
            test_uuid = generate_test_uuid()
            os.makedirs(f"{STORAGE_PATH}/{test_uuid}")
            logger.info('Directory created at: ' + f"{STORAGE_PATH}/{test_uuid}")
            received_json_data = json.loads(request.body.decode())
            try:
                test_ymls, initial_variable_dictionary = __extract_test_data(test_uuid, received_json_data['test'])
            except BadArgumentsError as e:
                return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)
            pool_executor = ThreadPoolExecutor(max_workers=1)
            try:
                pool_executor.submit(thread_executor, test_ymls, initial_variable_dictionary, test_uuid,
                                     received_json_data['email'])
                logger.info("task submitted to thread pool executor")
            except Exception as e:
                logger.error("Exception occurred", e)
            response_message = "Your Test UUID is: " + test_uuid + ". We'll send you an email with report shortly"
            return HttpResponse(response_message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception caught", exc_info=True)
            return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def retriever(request, testuuid):
    """
    Receives GET request and returns relevant data from the database

    """
    errors=[]
    testresults=[]
    if request.method == 'GET':
        try:
            logger.info("GET request recieved")
            if(TEST_RESULT_DB!= None and TEST_RESULT_DB.lower() == 'postgres'):
                results_for_given_testuuid=TestResults.objects.all().filter(TestUUID=testuuid).values()
                if request.body and results_for_given_testuuid:
                    testnames=json.loads(request.body)
                    for testname in testnames:
                        results_for_given_testname=TestResults.objects.all().filter(TestUUID=testuuid, TestName=testname["name"]).values()
                        if results_for_given_testname:
                            testresults.append(results_for_given_testname[0])
                        else:
                            wrong_test_name=testname["name"]
                            wrong_test_id=testuuid
                            errors.append(f"Bad Request : No Test in the TestUUID {wrong_test_id} is with TestName {wrong_test_name} ")
                            logger.error(f"Bad Request : No Test in the TestUUID {wrong_test_id} is with TestName {wrong_test_name} ")            
                else:
                    if results_for_given_testuuid:
                        for testresult in results_for_given_testuuid:
                            testresults.append(testresult)
                    else:
                        wrong_test_id=testuuid
                        logger.error(f"Bad Request : No Test with the TestUUID {wrong_test_id} ")
                        errors.append(f"Bad Request : No Test with the TestUUID {wrong_test_id} ")
                
                if(errors):
                    testresults.clear()
                    fetched_test_results=GetTestResults(testresults,errors)
                    fetched_test_results_json_string = json.dumps(fetched_test_results.__dict__, default=str)
                    fetched_test_results_json=json.loads(fetched_test_results_json_string)
                    logger.error(f"Bad Request : {fetched_test_results_json}")
                    return JsonResponse(fetched_test_results_json,status=status.HTTP_400_BAD_REQUEST)
                else:
                    fetched_test_results=GetTestResults(testresults,errors)
                    fetched_test_results_json_string = json.dumps(fetched_test_results.__dict__, default=str)
                    fetched_test_results_json=json.loads(fetched_test_results_json_string)
                    logger.info(f"Returning data : {fetched_test_results_json}")
                    return JsonResponse(fetched_test_results_json)
                
            else:
                logger.error("Database Functionality is not opted for.Hence GET request can't be processed")
                return HttpResponse("Database Functionality is not opted for.Hence GET request can't be processed",status=status.HTTP_400_BAD_REQUEST)
        except:
            logger.error("Exception caught", exc_info=True)
            return HttpResponse("error", status=status.HTTP_400_BAD_REQUEST)
    else :
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def __extract_test_data(test_uuid, test):
    initial_variable_dictionary = {}
    if "variables" in test:
        initial_variable_dictionary = test['variables']
    test_ymls = []
    source_location = test['source']
    location_type = test['type']
    path = test['path']
    if "git" in source_location.lower():
        if "file" == location_type:
            files = [path]
        else:
            files = get_yml_files_in_folder_git(REPO_NAME, BRANCH_NAME, path)
        for file_path in files:
            test_yml = read_yaml(REPO_NAME, BRANCH_NAME, file_path, test_uuid)
            test_ymls.append(test_yml)

    elif "local" in source_location.lower():
        if "file" == location_type:
            files = [path]
        else:
            files = get_yml_files_in_folder_local(path)
        for file_path in files:
            test_yml = read_local_yaml(file_path)
            test_ymls.append(test_yml)

    else:
        error_message = "source_location = %s is not supported, please use git or local" % source_location
        logger.error(error_message)
        raise UnsupportedFileSourceError(error_message)

    return test_ymls, initial_variable_dictionary
