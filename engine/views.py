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

from .models import TestExecutor
from .selenium_helper import browser_config
from .executor import execute_test
from .utils.utils import read_yaml, read_local_yaml
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
            data_file_location = received_json_data['fileLocation']
            initial_variable_dictionary = {}
            if "variables" in received_json_data:
                variable_data = received_json_data['variables']
                for key, value in variable_data.items():
                    initial_variable_dictionary[key] = value
            if "git" in data_file_location.lower():

                repo_name = REPO_NAME
                branch_name = BRANCH_NAME
                test_yml_content = read_yaml(repo_name, branch_name, received_json_data['file'], test_id)

            elif "local" in data_file_location.lower():
                test_yml_content = read_local_yaml(received_json_data['file'])
            else:
                logger.error("fileLocation is not supported, please use git or local")
                return HttpResponse("fileLocation is not supported, please use git or local",
                                    status=status.HTTP_400_BAD_REQUEST)
            web_driver = browser_config(test_yml_content['config'])
            test_executor = TestExecutor(1, test_id, initial_variable_dictionary, web_driver)
            pool_executor = ThreadPoolExecutor(max_workers=1)
            try:
                pool_executor.submit(execute_test, test_executor, test_yml_content['task'], test_yml_content['name'],
                                     received_json_data['email'])
                logger.info("task submitted")
            except Exception as e:
                logger.error("Excepption occured", e)
            response_message = "Your test ID is: " + test_id + ". We'll send you an email with report shortly"
            return HttpResponse(response_message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception caught", exc_info=True)
            return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
