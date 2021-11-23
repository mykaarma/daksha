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
from .alert_sender import *
from .method_mapper import *
from .selenium_helper import *
from .testreport_generator import *
from .email_generator import *

from daksha.settings import APACHE_URL
from .variable_dictionary import *
import jinja2
import ast
web_driver = None  # Assume a global webdriver which'll be used by all selenium methods


def execute_test(task, test_id, name, email, alert_channel_type):
    """
    Calls method to execute the steps mentioned in YAML and calls methods for report generation and sending test report email
     :param task: Test steps mentioned in YAML
     :type task: dict
     :param test_id: ID of the Test
     :type test_id: str
     :param name: Name of the Test Fetched From YAML
     :type name: str
     :param email: The email where the report will be sent
     :type email: str
    """
    try:
        execution_result, error_stack = True, None
        step = {}
        for step in task:
            execution_result, error_stack = execute_step(step, test_id)
            if execution_result is False:
                break
        if execution_result:
            logger.info("Test successful")
        else:
            logger.info("Test failed for test ID: " + test_id)
            send_alert(test_id,name,step,error_stack,alert_channel_type)

        logger.info("Test finished, sending report now")
        generate_result(test_id, execution_result, name, step, error_stack)
        report_url = APACHE_URL + test_id + '/report.html'
        send_report_email(test_id, report_url, email)

    except Exception as e:
        logger.error("Error encountered in executor: ", exc_info=True)


def execute_config(config):
    # Executor must maintain the webdriver variable, i.e., all selenium methods should ask for webdriver in method
    # params Setting webdriver configurations
    """
    Calls method for configuring the browser in accordance with specifications mentioned in YAML
     :param config: Configurations mentioned in YAML
     :type config: dict
    """
    global web_driver
    web_driver = browser_config(config)
    web_driver.maximize_window()
    web_driver.implicitly_wait(30)


def execute_step(step, test_id):
    """
    Executes steps mentioned in YAML
     :param step: Test steps mentioned in YAML
     :type step: dict
     :param test_id: ID of the Test
     :type test_id: str
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
            execution_success, error_stack = method_map[step](test_id, web_driver)
        elif isinstance(step, dict):
            logger.info("Gonna render the variables")
            #raise error if a variable present in yml file but not present in variable dictionary
            template = jinja2.Template(str(step),undefined=jinja2.StrictUndefined)
            step_render = template.render(variable_dictionary) #rendered the variables from the variable dictionary
            step = ast.literal_eval(step_render)  #converting the final string with rendered variables to dictionary step
            logger.info("Gonna call this method with args")
            for k, v in step.items():
                logger.info(str(type(v)) + "\t. " + str(v))
                execution_success, error_stack = method_map[k](test_id=test_id, web_driver=web_driver, **v)
                break
            logger.info("fin")
        if execution_success is False:
            return False, error_stack
        else:
            return True, error_stack
    except Exception as e:
        logger.error("Error encountered: ", exc_info=True)
        return False, traceback.format_exc()
