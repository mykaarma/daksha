"""
Daksha
Copyright (C) 2022 myKaarma.
opensource@mykaarma.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty tof
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from concurrent.futures.thread import ThreadPoolExecutor
from engine.executor import execute_test
from .email_generator import send_report_email
from .logs import *
from daksha.settings import APACHE_URL
from .models import TestExecutor
from .testreport_generator import generate_report


def thread_executor(test_ymls, initial_variable_dictionary, test_id, email):
    with ThreadPoolExecutor(max_workers=3) as pool_executor:
        for test_yml in test_ymls:
            try:
                test_executor = TestExecutor(1, test_id, initial_variable_dictionary, test_yml, None)
                pool_executor.submit(execute_test, test_executor, email)
                logger.info("Task submitted")
            except Exception as e:
                logger.error("Exception occurred", e)
            pass
    logger.info("All threads complete, generating test report")
    generate_report(test_id)
    report_url = APACHE_URL + test_executor.test_id + '/report.html'
    send_report_email(test_executor.test_id, report_url, email)

