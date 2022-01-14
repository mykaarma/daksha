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
from jinja2 import UndefinedError

from .method_mapper import *
from .models import TestExecutor
from .selenium_helper import *
from .testreport_generator import *
from .email_generator import *

from daksha.settings import APACHE_URL
import jinja2
import ast


def execute_test(test_executor: TestExecutor, task, name, email):
    """
    Calls method to execute the steps mentioned in YAML and calls methods for report generation and sending test report email
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :param task: Test steps mentioned in YAML
     :type task: dict
     :param name: Name of the Test Fetched From YAML
     :type name: str
     :param email: The email where the report will be sent
     :type email: str
    """
    try:
        execution_result, error_stack = True, None
        step = {}
        for step in task:
            execution_result, error_stack = execute_step(test_executor, step)
            if execution_result is False:
                break
        if execution_result:
            logger.info("Test successful")
        else:
            logger.info("Test failed for test ID: " + test_executor.test_id)

        logger.info("Test finished, sending report now")
        generate_result(test_executor.test_id, execution_result, name, step, error_stack)
        report_url = APACHE_URL + test_executor.test_id + '/report.html'
        send_report_email(test_executor.test_id, report_url, email)

    except Exception:
        logger.error("Error encountered in executor: ", exc_info=True)


def execute_step(test_executor: TestExecutor, step):
    """
    Executes steps mentioned in YAML
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :param step: Test steps mentioned in YAML
     :type step: dict
     :raises : KeyError
     :returns: Status of Execution and error stack
     :rtype: tuple
    """
    try:
        logger.info("Executing:\t" + str(type(step)) + '\t' + str(step))
        # https://stackoverflow.com/a/40219576
        # https://note.nkmk.me/en/python-argument-expand/
        execution_success = False
        error_stack = None
        if isinstance(step, str):
            logger.info("Gonna process the method directly")
            execution_success, error_stack = method_map[step](test_executor=test_executor)
        elif isinstance(step, dict):
            logger.info("Gonna render the variables")
            # raise error if a variable present in yml file but not present in variable dictionary
            template = jinja2.Template(str(step), undefined=jinja2.StrictUndefined)
            # rendered the variables from the variable dictionary
            step_render = template.render(test_executor.variable_dictionary)
            # converting the final string with rendered variables to dictionary step
            step = ast.literal_eval(step_render)
            logger.info("Gonna call this method with args")
            for k, v in step.items():
                logger.info(str(type(v)) + "\t. " + str(v))
                execution_success, error_stack = method_map[k](test_executor=test_executor, **v)
                break
            logger.info("fin")
        if execution_success is False:
            return False, error_stack
        else:
            return True, error_stack
    except UndefinedError as e:
        logger.error("Error in rendering variable: ", exc_info=True)
        return False, "Error in rendering variable: " + str(e)
    except Exception:
        logger.error("Error encountered: ", exc_info=True)
        return False, traceback.format_exc()
