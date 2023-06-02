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
from daksha.settings import ALERT_URL
from .logs import *
import requests
from string import Template


def gchat_alert(test_uuid, name, step, error_stack):
    alert_body = "Test Case: " + name + " failed for test id : " + test_uuid + "\n _ERROR_  :  ```" + error_stack.replace(
        '"', "") + "```" + "\n in _step_ ```" + step.replace('"', "") + "```"
    if len(ALERT_URL) == 0:
        logger.info('Alert not sent, ALERT_URL  not set')
        return
    else:
        alert_template = Template(open("templates/gchat_alert.json", "r").read())
        return requests.post(ALERT_URL, data=alert_template.substitute(body=alert_body))


def slack_alert(test_uuid, name, step, error_stack):
    alert_body = "Test Case: " + name + " failed for test id : " + test_uuid + "\n _ERROR_  :  ```" + error_stack.replace(
        '"', "") + "```" + "\n in _step_ ```" + step.replace('"', "") + "```"
    headers = {'content-type': 'application/json'}
    if len(ALERT_URL) == 0:
        logger.info('Alert not sent, ALERT_URL  not set')
        return
    else:
        alert_template = Template(open("templates/slack_alert.json", "r").read())
        return requests.post(ALERT_URL, data=alert_template.substitute(body=alert_body), headers=headers)


switcher = {
    "gchat": gchat_alert,
    "slack": slack_alert
}


def send_alert(test_uuid, name, step, error_stack, alert_type):
    
    func = switcher.get(alert_type, "no_alert")
    if (alert_type == None) or (len(alert_type) == 0):
        return
    elif func == "no_alert":
        logger.warn("Supported alert type not found,alert types supported: " + str(list(switcher.keys())))
    else:
        return func(test_uuid, name, step, error_stack)
