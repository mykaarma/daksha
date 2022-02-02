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
import string
import random

from .logs import logger

from daksha.settings import STORAGE_PATH
from .models import TestResult
from datetime import datetime


def generate_result(test_id, response, name, step, error_stack):
    """
    Generates Test Result
     :param test_id: ID of the Test
     :type test_id: str
     :param response: Execution Status
     :type response: bool
     :param step : Last executed step of the Test
     :type step: dict
     :param error_stack: Error Stack if Test failed
     :type error_stack: str
     :param name: Name of the Test mentioned in YAML
     :type name: str
    """
    try:
        logger.info('Creating test result')
        time_now = datetime.now()
        result_file_path = f"{STORAGE_PATH}/{test_id}/result/{name}_{time_now}"
        os.makedirs(os.path.dirname(result_file_path), exist_ok=True)
        # result_file = open(result_file_path, "a")
        if response:
            test_status = "Passed"
            step = ""
            error_stack = ""

        else:
            test_status = "Failed"
            # error_stack=error_stack.replace("\n", " ")
        test_result = TestResult(name, test_status, step.__str__(), error_stack)
        # json.loads(result_file).update(test_report)
        logger.info(test_result.__dict__)
        # result_file.write(test_report)
        # logger.info('Report created at ' + report_file_path)
        with open(result_file_path, 'w') as f:
            json.dump(test_result.__dict__, f)
        f.close()
    except Exception:
        logger.error("Error in testreport generation:", exc_info=True)


def generate_test_id():
    """
    Generates an unique 11 Digit Test ID
     :returns : 11 Digit unique Test ID
     :rtype: str
    """
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=11))
    logger.info("Test ID: " + res)
    return res


def generate_report(test_id):
    """
    Generates Test Report
     :param test_id: ID of the Test
     :type test_id: str
    """
    logger.info('Creating test report')
    report_file_path = f"{STORAGE_PATH}/{test_id}/report.html"
    report_file = open(report_file_path, "w")
    result_folder_path = f"{STORAGE_PATH}/{test_id}/result"
    passed_count, failed_count = 0, 0
    test_result = []
    for file in os.listdir(result_folder_path):
        result_file_path = os.path.join(result_folder_path, file)
        with open(result_file_path) as f:
            for line in f:
                test_result.append(json.loads(line.strip()))
                logger.info(line.strip())
                if json.loads(line)["test_status"] == "Passed":
                    passed_count += 1
                else:
                    failed_count += 1

    test_result = json.dumps(test_result)
    report_template = open("templates/test_report_template.html", "r").read()
    replacement = {"${test_id}": test_id, "${test_result}": test_result, "${passed_count}": passed_count.__str__(),
                   "${failed_count}": failed_count.__str__()}
    for key, value in replacement.items():
        report_template = report_template.replace(key, value)
        logger.info(key)
    report_file.write(report_template)
    report_file.close()
