import concurrent
from concurrent.futures.thread import ThreadPoolExecutor

from engine.executor import execute_test
from .email_generator import send_report_email
from .logs import *
from daksha.settings import STORAGE_PATH, APACHE_URL
from .models import TestExecutor
from .testreport_generator import generate_report


def thread_executor(test_ymls, initial_variable_dictionary, test_id, email):
    futures = []

    with ThreadPoolExecutor(max_workers=5) as pool_executor:
        for test_yml in test_ymls:
            try:
                test_executor = TestExecutor(1, test_id, initial_variable_dictionary, test_yml, None)
                futures.append(pool_executor.submit(execute_test, test_executor, email))
                logger.info("Task submitted")
            except Exception as e:
                logger.error("Exception occurred", e)
            pass
    logger.info("All threads complete, generating test report")
    generate_report(test_id)
    report_url = APACHE_URL + test_executor.test_id + '/report.html'
    send_report_email(test_executor.test_id, report_url, email)

