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

import traceback
import time
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from .logs import logger
from .models import TestExecutor
from .utils.screenshot_utils import take_screenshot


def browser_config(config) -> WebDriver:
    """
    Configures the browser in accordance with mentioned specifications(env,browser,driverAddress) in YAML
     :param config: Browser configuration fetched from YAML
     :type config: dict
     :returns: Configured Webdriver
     :rtype: object
     :raises: exception
    """

    try:
        env = config['env']
        brow = config['browser']
        path = config['driverAddress']
    except KeyError:
        raise Exception(
            "Ill formatted arguments, 'env', 'browser' and 'driverAddress' must be present in the list of args")
    if brow.lower() == 'chrome' and env.lower() == 'local':
        web_driver = webdriver.Chrome(executable_path=path)
    elif brow.lower() == 'chrome' and env.lower() == 'remote':
        options = webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=800,600")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        web_driver = webdriver.Remote(
            command_executor=path,
            desired_capabilities=DesiredCapabilities.CHROME,
            options=options,
        )
    else:
        logger.error("Browser or env not supported at this time")
        raise Exception("Browser or env not supported at this time")

    web_driver.maximize_window()
    web_driver.implicitly_wait(30)
    logger.info(brow + ' browser launched on ' + env)
    return web_driver


def launch_browser(test_executor: TestExecutor):
    """
    Launches the browser
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :returns: Status of execution
     :rtype: tuple
    """
    logger.info("I'll launch the browser")
    # Got nothing to do. Shouldn't exist :p
    return True, None


def quit_browser(test_executor: TestExecutor):
    """
    Quits the browser
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :returns: Status of execution
     :rtype: tuple
    """
    logger.info("I'll quit the browser")
    test_executor.web_driver.quit()
    return True, None


def open_url(test_executor: TestExecutor, **kwargs):
    """
     Opens url mentioned in YAML
      :param test_executor: The TestExecutor object to give context for execution
      :type test_executor: TestExecutor
      :param kwargs: WebElement Description Fetched From YAML
      :type kwargs: dict
      :returns: Status of execution and error stack
      :rtype: tuple
    """
    try:
        url = kwargs['url']
    except KeyError:
        return False, "Ill formatted arguments, 'url' must be present in the list of args"
    logger.info("I'll open it's url")
    logger.info(url)
    test_executor.web_driver.get(url)
    take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
    return True, None


# improve this to accept any element identifier, not just xpath
def fill_data(test_executor: TestExecutor, **kwargs):
    """
     Fills data in the position located by WebElement.Location is fetched from YAML
      :param test_executor: The TestExecutor object to give context for execution
      :type test_executor: TestExecutor
      :param kwargs : WebElement Description Fetched From YAML
      :type kwargs : dict
      :returns: Status of execution and error stack if exception is encountered
      :rtype: tuple
     """
    try:
        value = kwargs['value']
    except KeyError:
        return False, "Ill formatted arguments, 'value' must be present in the list of args"
    locator, locator_value = get_locator_info(**kwargs)
    logger.info("I'll fill data in input box")
    error_stack = None
    for i in range(5):
        try:
            element = WebDriverWait(test_executor.web_driver, 10).until(
                EC.visibility_of_element_located((locator, locator_value))
            )
            element.clear()
            element.send_keys(value)
            logger.info("Data filled successfully")
            take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
            return True, None
        except Exception as e:
            error_stack = traceback.format_exc()
            logger.error("Attempt " + str(i) + " to fill input failed")
    return False, error_stack


def select_in_dropdown(test_executor: TestExecutor, **kwargs):
    """
    Selects a value from the dropdown
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :param kwargs: WebElement Description Fetched From YAML
     :type kwargs: dict
     :returns: Status of execution and error stack
     :rtype: tuple
    """
    try:
        value = kwargs['value']
    except KeyError:
        return False, "Ill formatted arguments, 'value' must be present in the list of args"
    locator, locator_value = get_locator_info(**kwargs)
    logger.info("I'll select value from drop-down")
    error_stack = None
    for i in range(5):
        try:
            element = WebDriverWait(test_executor.web_driver, 10).until(
                EC.visibility_of_element_located((locator, locator_value))
            )
            select = Select(element)
            select.select_by_visible_text(value)
            logger.info("Dropdown selected successfully")
            take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
            return True, None
        except Exception as e:
            error_stack = traceback.format_exc()
            logger.error("Attempt " + str(i) + " to select dropdown failed")
    return False, error_stack


# improve this to accept any element identifier, not just xpath
def click_button(test_executor: TestExecutor, **kwargs):
    """
    Click the button using webelement locator passed in kwargs
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :param kwargs: WebElement Description Fetched From YAML
     :returns: Status of execution and error stack
     :rtype: object

    """
    locator, locator_value = get_locator_info(**kwargs)
    logger.info("I'll click a button!")
    error_stack = None
    # try for 5 times
    for i in range(5):
        try:
            element = WebDriverWait(test_executor.web_driver, 10).until(
                EC.element_to_be_clickable((locator, locator_value))
            )
            element.click()
            logger.info("Click successful")
            take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
            return True, None
        except Exception as e:
            error_stack = traceback.format_exc()
            logger.error("Attempt " + str(i) + " to click failed")
    return False, error_stack


def validate_ui_element(test_executor: TestExecutor, **kwargs):
    """
    Validates a UI element
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :param kwargs: WebElement Description Fetched From YAML
     :returns: Status of execution and Failure String
     :rtype: tuple
    """
    try:
        mode = kwargs['mode']
        value = kwargs['value']
    except KeyError:
        return False, "Ill formatted arguments, 'mode' and 'value' must be present in the list of args"
    locator, locator_value = get_locator_info(**kwargs)
    logger.info("I'll verify a UI element!")
    # try for 5 times
    validation_result = False
    for i in range(5):
        try:
            element = WebDriverWait(test_executor.web_driver, 10).until(
                EC.visibility_of_element_located((locator, locator_value))
            )
            elementTag = element.tag_name
            if elementTag == "input":
                element_value = element.get_attribute("value")
                logger.info("Validating input textbox text to: "+element_value)
            else:
                element_value = element.text
                logger.info("Validating text to: "+element_value)
            take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
            if mode == 'equals':
                validation_result = (value == element_value)
            elif mode == 'contains':
                validation_result = str(element_value).__contains__(value)
            elif mode == 'not_contains':
                validation_result = not str(element_value).__contains__(value)
            else:
                validation_result = False
            if validation_result is True:
                break
            else:
                logger.info("Value found " + element_value + " did not match value given: " + value + ", mode=" + mode)

        except Exception as e:
            logger.error("Attempt " + str(i) + " for validation failed \n", exc_info=True)

    return validation_result, "Failed Validation"


def switch_iframe(test_executor: TestExecutor, **kwargs):
    """
    Switches iframe to the one specified by WebElement locator in YAML
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :param kwargs: WebElement Description Fetched From YAML
     :type kwargs: dict
     :returns: Status of execution and error stack
     :rtype: tuple
    """
    locator, locator_value = get_locator_info(**kwargs)
    try:
        element = WebDriverWait(test_executor.web_driver, 10).until(
            EC.visibility_of_element_located((locator, locator_value))
        )
        test_executor.web_driver.switch_to.frame(element)
        logger.info("switched successful to frame. " + locator + " = " + locator_value)
        take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
        return True, None
    except Exception as e:
        logger.error("switch to frame failed \n", exc_info=True)
        return False, traceback.format_exc()


def switch_to_default_iframe(test_executor: TestExecutor):
    """
    Switch to default iframe
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :returns: Status of execution
     :rtype: tuple
    """
    test_executor.web_driver.switch_to.default_content()
    take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
    logger.info("switched successful to default window")
    return True, None


def refresh_page(test_executor: TestExecutor):
    """
    Refresh the webpage
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :returns: Status of execution
     :rtype: tuple
    """
    test_executor.web_driver.refresh()
    take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
    logger.info("Page refreshed successfully")
    return True, None


def navigate_back(test_executor: TestExecutor):
    """
    Navigate Back to previous page
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :returns: Status of execution
     :rtype: tuple
    """
    test_executor.web_driver.back()
    take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
    logger.info("User navigated Back successfully")
    return True, None


def open_new_tab(test_executor: TestExecutor):
    """
     Opens a new tab
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
      :returns: Status of execution and error stack
      :rtype: object
     """
    test_executor.web_driver.execute_script("window.open()")
    test_executor.web_driver.switch_to_window(
        test_executor.web_driver.window_handles[len(test_executor.web_driver.window_handles) - 1])
    take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
    logger.info("Switched to new Tab successfully")
    return True, None


def switch_to_tab(test_executor: TestExecutor, **kwargs):
    """
    Switches Tab to that mentioned in YAML
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :param kwargs: WebElement Description Fetched From YAML
     :type kwargs: dict
     :returns; Status of Execution and error stack

    """
    is_tab_switched = False
    if "title" in kwargs.keys():
        value = kwargs["title"]
        for handle in test_executor.web_driver.window_handles:
            test_executor.web_driver.switch_to_window(handle)
            if value in test_executor.web_driver.title:
                is_tab_switched = True
                logger.info("Switched to tab with {} as {} : ".format("title", value))
                break
    elif "index" in kwargs.keys():
        try:
            value = int(kwargs["index"])
            test_executor.web_driver.switch_to_window(test_executor.web_driver.window_handles[value])
            logger.info("Switched to tab indexed as : " + str(value))
            is_tab_switched = True
            logger.info("Switched to tab with {} as {} : ".format("index", str(value)))
        except Exception as e:
            error_stack = traceback.format_exc()
            return False, error_stack
    else:
        return False, "Ill formatted arguments, either 'title' or 'index' must be present in the list of args"
    take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)

    return is_tab_switched, None


def wait_for(test_executor: TestExecutor, **kwargs):
    """
    Waits for an UI element or specified time
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :param kwargs: WebElement Description/wait-time Fetched From YAML
     :returns: Status of execution and Failure String
     :rtype: tuple
    """
    try:
        mode = kwargs['mode']
    except KeyError:
        return False, "Ill formatted arguments, 'mode' must be present in the list of args"
    wait_result = False
    if mode in ["visibility", "invisibility"]:
        locator, locator_value = get_locator_info(**kwargs)
        logger.info("I'll wait for an UI element!")
        error = None
        wait = WebDriverWait(test_executor.web_driver, 10, poll_frequency=1,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        for i in range(5):
            try:
                if mode == "visibility":
                    wait.until(
                        EC.visibility_of_element_located((locator, locator_value))
                    )
                    wait_result = True
                elif mode == "invisibility":
                    wait.until(
                        EC.invisibility_of_element_located((locator, locator_value))
                    )
                    wait_result = True
                break
            except Exception as e:
                logger.error("Attempt " + str(i) + " for waiting for " + mode + " of " + locator + " failed \n",
                             exc_info=True)
        if not wait_result:
            error = "Waiting for " + mode + " of " + locator + + " " + locator_value + " failed"
        return wait_result, error
    elif mode == "hardwait":
        try:
            value = kwargs['value']
        except KeyError:
            return False, "Ill formatted arguments, 'value' must be present in the list of args for mode : hardwait"
        logger.info("I'll wait " + str(value) + " seconds")
        time.sleep(value)
        return True, None
    else:
        logger.error("Mode not supported.Please enter in [hardwait, visibility, invisibiltiy]")
        error = "Ill formatted argument, supported modes : [hardwait, visibility, invisibiltiy]"
        return False, error


def capture_ui_element(test_executor: TestExecutor, **kwargs):
    """
    Captures a UI element to save it in variable_dictionary of test_executor
    :param test_executor: The TestExecutor object to give context for execution
    :type test_executor: TestExecutor
    :param kwargs: WebElement Description/wait-time Fetched From YAML
    :returns: Status of execution and Failure String
    :rtype: tuple
    """
    locator, locator_value = get_locator_info(**kwargs)
    try:
        save_in = kwargs['save_in']
    except KeyError:
        return False, "Ill formatted arguments, 'save_in' must be present in the list of args"
    element = WebDriverWait(test_executor.web_driver, 10).until(
        EC.element_to_be_clickable((locator, locator_value))
    )
    take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
    elementTag = element.tag_name
    if elementTag == "input":
        element_value = element.get_attribute("value")
        logger.info("Capturing input texbox text " + element_value)
    else:
        element_value = element.text
        logger.info("Capturing text " + element_value)
    test_executor.variable_dictionary[save_in] = element_value
    logger.info("saved text from UI element. variable: {}, value: {}".format(save_in, element_value))
    return True, None


def get_locator_info(**kwargs):
    """
    Gets the locator type and locator info
     :param kwargs: WebElement Description Fetched From YAML
     :type kwargs: dict
     :raises: exception
     :returns : Locator type and Locator
     :rtype: tuple
    """
    if 'id' in kwargs.keys():
        return By.ID, kwargs['id']
    elif 'css' in kwargs.keys():
        return By.CSS_SELECTOR, kwargs['css']
    elif 'classname' in kwargs.keys():
        return By.CLASS_NAME, kwargs['classname']
    elif 'xpath' in kwargs.keys():
        return By.XPATH, kwargs['xpath']
    elif 'linktext' in kwargs.keys():
        return By.LINK_TEXT, kwargs['linktext']
    elif 'partiallinktext' in kwargs.keys():
        return By.PARTIAL_LINK_TEXT, kwargs['partiallinktext']
    elif 'name' in kwargs.keys():
        return By.NAME, kwargs['name']
    else:
        raise Exception("Invalid locator passed")


def scroll_to(test_executor: TestExecutor, **kwargs):
    """
    Scrolls down to a particular element's view
     :param test_executor: The TestExecutor object to give context for execution
     :type test_executor: TestExecutor
     :param kwargs: WebElement Description Fetched From YAML
     :type kwargs: dict
     :returns: Status of execution and error stack
     :rtype: tuple
    """
    locator, locator_value = get_locator_info(**kwargs)
    logger.info("I'll scroll to element")
    error_stack = None
    for i in range(5):
        try:
            element = WebDriverWait(test_executor.web_driver, 10).until(
                EC.visibility_of_element_located((locator, locator_value))
            )
            test_executor.web_driver.execute_script("arguments[0].scrollIntoView();", element)
            logger.info("Scrolled to element successfully")
            take_screenshot(test_executor.test_id, test_executor.test_yml["name"], test_executor.web_driver)
            return True, None
        except Exception as e:
            error_stack = traceback.format_exc()
            logger.error("Attempt " + str(i) + " to scroll to element failed")
    return False, error_stack

