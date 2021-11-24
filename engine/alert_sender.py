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


def gchat_alert(test_id, name, step, report_url, error_stack):
    alert_body = "Test Case: " + name + " failed for test id : " + test_id + "\n _ERROR_  :  ```" + error_stack.replace(
        '"', "") + "```" + "\n in _step_ ```" + step.replace('"', "") + "```"
    logger.info(alert_body)
    if len(ALERT_URL) == 0:
        logger.info('Alert not sent, ALERT_URL  not set')
        return
    else:
        alert_template = Template(open("templates/gchat_alert.json", "r").read())
        return requests.post(ALERT_URL, data=alert_template.substitute(body=alert_body,
                                                                       reportlink=report_url))


switcher = {
    "gchat": gchat_alert
}


def send_alert(test_id, name, step, error_stack, report_url, alert_type):
    # Get the function from switcher dictionary
    func = switcher.get(alert_type, "no_alert")
    # Execute the function

    if (alert_type == None) or (len(alert_type) == 0):
        return
    elif func == "no_alert":
        logger.warn("Supported alert type not found,alert types suppoorted: " + str(switcher.keys()))
    else:
        return func(test_id, name, step, report_url, error_stack)
