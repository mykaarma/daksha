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

import string
import random

from .logs import logger

from daksha.settings import STORAGE_PATH


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
        logger.info('Creating test report')
        report_file_path = f"{STORAGE_PATH}/{test_id}/report.html"
        report_file = open(report_file_path, "w")
        if response:
            result = 'Passed'
            report_template = open("templates/testReport.html", "r").read()
            test_report = report_template.format(test_ID=test_id, test_name=name, test_result=result)

        else:
            result = 'Failed'
            report_template = open("templates/test_report_fail.html", "r").read()
            test_report = report_template.format(test_ID=test_id, test_name=name, test_result=result, test_step=step,
                                                 error=error_stack)
        report_file.write(test_report)
        logger.info('Report created at ' + report_file_path)
        report_file.close()
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
