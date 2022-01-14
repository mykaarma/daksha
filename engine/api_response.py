"""
Daksha
Copyright (C) 2021 myKaarma.
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

import requests
import jmespath
from requests.auth import HTTPBasicAuth, HTTPDigestAuth, HTTPProxyAuth

from .logs import logger
from json import JSONDecodeError
from django.http import HttpResponse
from rest_framework import status

from .models import TestExecutor


def get_arguments_info(param: str, **kwargs):
    """
    get arguments info to that mentioned in YAML
     :param param: Parameter
     :type param: object
     :param kwargs: WebElement Description Fetched From YAML
     :type kwargs: dict
     :returns; Parameter in the YAML or None

    """
    if param in kwargs.keys():
        return kwargs[param]
    else:
        return None


def get_authentication_(**kwargs):
    """
    get authentication info to that mentioned in YAML
     :param kwargs: WebElement Description Fetched From YAML
     :type kwargs: dict
     :returns; Authentication Mode with username and password or None

    """
    auth = get_arguments_info('auth', **kwargs)
    if auth is None:
        return None
    if auth["type"] == "Basic":
        return HTTPBasicAuth(auth["username"], auth["password"])
    elif auth["type"] == "Proxy":
        return HTTPProxyAuth(auth["username"], auth["password"])
    elif auth["type"] == "Digest":
        return HTTPDigestAuth(auth["username"], auth["password"])


def make_http_request(test_executor: TestExecutor, **kwargs):
    """
    makes the http request to that mentioned in YAML
    :param test_executor: The TestExecutor object to give context for execution
    :type test_executor: TestExecutor
    :param kwargs: WebElement Description Fetched From YAML
    :type kwargs: dict
    :returns; Response of the Request made

    """
    if kwargs['request'] == 'GET':
        r = requests.get(kwargs['url'], json=get_arguments_info('payload', **kwargs),
                         headers=get_arguments_info('headers', **kwargs),
                         auth=get_authentication_(**kwargs), cookies=get_arguments_info('cookies', **kwargs),
                         proxies=get_arguments_info('proxy', **kwargs), timeout=get_arguments_info('timeout', **kwargs))
        return process_response(test_executor, r, **kwargs)
    elif kwargs['request'] == 'POST':
        r = requests.post(kwargs['url'], data=get_arguments_info('data', **kwargs),
                          json=get_arguments_info('data', **kwargs),
                          headers=get_arguments_info('headers', **kwargs), auth=get_authentication_(**kwargs),
                          cookies=get_arguments_info('cookies', **kwargs),
                          proxies=get_arguments_info('proxy', **kwargs),
                          timeout=get_arguments_info('timeout', **kwargs))
        return process_response(test_executor, r, **kwargs)
    elif kwargs['request'] == 'PUT':
        r = requests.put(kwargs['url'], data=get_arguments_info('payload', **kwargs),
                         json=get_arguments_info('payload', **kwargs),
                         headers=get_arguments_info('headers', **kwargs), auth=get_authentication_(**kwargs),
                         cookies=get_arguments_info('cookies', **kwargs), proxies=get_arguments_info('proxy', **kwargs),
                         timeout=get_arguments_info('timeout', **kwargs))
        return process_response(test_executor, r, **kwargs)
    elif kwargs['request'] == 'DELETE':
        r = requests.delete(kwargs['url'], json=get_arguments_info('payload', **kwargs),
                            headers=get_arguments_info('headers', **kwargs),
                            auth=get_authentication_(**kwargs), cookies=get_arguments_info('cookies', **kwargs)
                            , proxies=get_arguments_info('proxy', **kwargs),
                            timeout=get_arguments_info('timeout', **kwargs))
        return process_response(test_executor, r, **kwargs)
    else:
        logger.error("Reuest method not supported :(")
        return False, HttpResponse("Reuest method not supported :(",
                                   status=status.HTTP_400_BAD_REQUEST)


def process_response(test_executor: TestExecutor, r, **kwargs):
    """
    processes the http request to that mentioned in YAML
    :param test_executor: The TestExecutor object to give context for execution
    :type test_executor: TestExecutor
    :param r: Request made
    :type r: request
    :param kwargs: WebElement Description Fetched From YAML
    :type kwargs: dict
    :returns; Status of Execution and error stack

    """
    response_dict = get_arguments_info('response', **kwargs)
    if response_dict is None:
        r.raise_for_status()
        return True, None
    if 'status' not in response_dict.keys():
        # use raiser_for_status() if the status code is not present
        # 2xx/3xx - pass; 4xx/5xx - raises error
        r.raise_for_status()
    else:
        # check if status_code matches the status provided 
        if r.status_code != response_dict['status']:
            logger.info(str(r.status_code) + " Status Not Matched :(")
            logger.info(r.text)
            return False, None
    logger.info(str(r.status_code) + " OK! Proceeding further")
    return save_response(test_executor, r, response_dict)


def save_response(test_executor: TestExecutor, r, response_dict):
    """
    processes the http request to that mentioned in YAML
    :param test_executor: The TestExecutor object to give context for execution
    :type test_executor: TestExecutor
    :type r: request
    :param response_dict: response dict fetched from YAML
    :type response_dict: dict
    :returns; Status of Execution and error stack

    """
    try:
        logger.info(r.json())
        if 'save' in response_dict:
            for entry in response_dict['save']:
                b = entry['save in']
                # if key is not present in dict, whole json will be saved to the 'save in' parameter
                if 'key' in entry:
                    test_executor.variable_dictionary[b] = jmespath.search(entry['key'], r.json())
                else:
                    test_executor.variable_dictionary[b] = r.text
            logger.info(str(test_executor.variable_dictionary) + "   new key, value pairs added")
    except JSONDecodeError:
        logger.info(r.text)
        # save the text response in the variable_dict
        if 'save' in response_dict:
            for entry in response_dict['save']:
                b = entry['save in']
                test_executor.variable_dictionary[b] = r.text
            logger.info(str(test_executor.variable_dictionary) + " new (key,value) pairs added;"
                                                            " value contains the whole text received")
    return True, None
