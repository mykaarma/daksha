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
from .logs import logger, get_logger
from daksha.settings import APACHE_URL,TEST_RESULT_DB, REPORT_PORTAL_ENABLED,REPORT_PORTAL_ENDPOINT, REPORT_PORTAL_PROJECT_NAME, REPORT_PORTAL_TOKEN
from reportportal_client import RPClient  # type: ignore
from .models import TestExecutor
from .testreport_generator import generate_report
from engine import test_result_utils
from reportportal_client.helpers import timestamp  # type: ignore

def thread_executor(test_ymls, initial_variable_dictionary, test_uuid, email):
    # Test Executor object initialization and store in a list
    testExecutorObjects=[]
    report_portal_service = None
    launch_id = None
    
    if(REPORT_PORTAL_ENABLED != None and REPORT_PORTAL_ENABLED.lower() == "true"):
        report_portal_service = RPClient(
            endpoint=REPORT_PORTAL_ENDPOINT,
            project=REPORT_PORTAL_PROJECT_NAME,
            token=REPORT_PORTAL_TOKEN
        )
        report_portal_service.start()
        logger.info("User has opted for Test Reports to be displayed on Report Portal")
        launch_id = report_portal_service.start_launch(name = f"Daksha_test_{test_uuid}", mode = 'DEFAULT', start_time = timestamp())
        logger.info(f"Initiating launch in Report Portal with name {test_uuid}")
        
    for test_yml in test_ymls:
        test_result_object = test_result_utils.initialize_test_result(test_uuid, test_yml)
        if(REPORT_PORTAL_ENABLED != None and REPORT_PORTAL_ENABLED.lower() == "true"):
            if 'labels' in test_yml and bool(test_yml['labels']):
                name = test_yml["name"]
                attributes = [{'key': key, 'value': value} for key, value in test_yml['labels'].items()]
                report_portal_test_id = report_portal_service.start_test_item(name = name, item_type = 'step', attributes=attributes, start_time = timestamp()) 
                logger.info(f"attributes with {report_portal_test_id} and {name} are {attributes}")
            else:
                report_portal_test_id = report_portal_service.start_test_item(name = test_yml["name"], item_type = 'step', start_time = timestamp()) 
                logger.info("Labels are not set in the test")
                
            # Create a dedicated logger per test with safety net
            try:
                test_executor_logger = get_logger(report_portal_service, report_portal_test_id)
            except Exception as e:
                logger.error("Failed to create dedicated logger: %s", e, exc_info=True)
                test_executor_logger = logger  # fallback to root logger

            test_executor = TestExecutor(1,test_uuid,initial_variable_dictionary,test_yml,None,test_result_object,report_portal_service,report_portal_test_id,test_executor_logger)
        else:
            test_executor= TestExecutor(1, test_uuid, initial_variable_dictionary, test_yml, None ,test_result_object)
        testExecutorObjects.append(test_executor)
    
    with ThreadPoolExecutor(max_workers=3) as pool_executor:
        for test_executor in testExecutorObjects:
            try:
                pool_executor.submit(execute_test, test_executor, email)
                if(TEST_RESULT_DB!= None and TEST_RESULT_DB.lower() == "postgres"):
                    test_executor.test_result.Status="In_Progress"
                    test_executor.test_result.save()
                logger.info("Task submitted")
            except Exception as e:
                logger.error("Exception occurred", e)
        pass

    if REPORT_PORTAL_ENABLED != None and REPORT_PORTAL_ENABLED.lower() == "true":
        report_portal_service.finish_launch(end_time = timestamp())
        logger.info(f"Tests finished. Ending launch Daksha_test_{test_uuid} in Report Portal ")
        report_portal_service.terminate()
        
    logger.info("All threads complete, generating test report")
    generate_report(test_uuid)
    report_url = APACHE_URL + test_executor.test_uuid + '/report.html'
    send_report_email(test_executor.test_uuid, report_url, email)

