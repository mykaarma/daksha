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

from concurrent.futures.thread import ThreadPoolExecutor
from django.http import HttpResponse
from rest_framework import status

from .errors import UnsupportedFileSourceError, BadArgumentsError
from .models import TestExecutor
from .executor import execute_test
from .utils.utils import read_yaml, read_local_yaml, get_yml_files_in_folder_local, get_yml_files_in_folder_git
from .testreport_generator import *
import json
from daksha.settings import REPO_NAME, BRANCH_NAME
import os


# Create your views here.
def executor(request):
    """
    Receives http request and starts execution of Test

    """
    if request.method == 'POST':
        try:
            test_id = generate_test_id()
            os.makedirs(f"{STORAGE_PATH}/{test_id}")
            logger.info('Directory created at: ' + f"{STORAGE_PATH}/{test_id}")
            received_json_data = json.loads(request.body.decode())
            try:
                test_ymls, initial_variable_dictionary = __extract_test_data(test_id, received_json_data['test'])
            except BadArgumentsError as e:
                return HttpResponse(str(e), status=status.HTTP_400_BAD_REQUEST)
            pool_executor = ThreadPoolExecutor(max_workers=5)
            for test_yml in test_ymls:
                try:
                    test_executor = TestExecutor(1, test_id, initial_variable_dictionary, None)
                    pool_executor.submit(execute_test, test_executor, test_yml, received_json_data['email'])
                    logger.info("task submitted")
                except Exception as e:
                    logger.error("Exception occurred", e)
                pass
            response_message = "Your test ID is: " + test_id + ". We'll send you an email with report shortly"
            return HttpResponse(response_message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception caught", exc_info=True)
            return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def __extract_test_data(test_id, test):
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
            test_yml = read_yaml(REPO_NAME, BRANCH_NAME, file_path, test_id)
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
