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
import logging
import os

from reportportal_client.helpers import timestamp
from daksha.settings import LOG_FILE,REPORT_PORTAL_ENABLED

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Logging configs
logFormatter = logging.Formatter('%(asctime)s [%(levelname)-7.7s]  %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

fileHandler = logging.FileHandler(LOG_FILE)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

def report_portal_logger(report_portal_service,report_portal_test_id,message,level,screenshot=None):
    if(REPORT_PORTAL_ENABLED != None and REPORT_PORTAL_ENABLED.lower() == "true"):
        if(screenshot == None):
            report_portal_service.log(level=level, message=message,time=timestamp(),item_id=report_portal_test_id)
            logger.info("Logs sents to Report Portal")       
        else:
            with open(screenshot, "rb") as file:
                screenshot_data = file.read()
            attachment={"data": screenshot_data, "mime": "image/png"}
            report_portal_service.log(level=level,message=message, attachment=attachment,time=timestamp() ,item_id=report_portal_test_id)
            logger.info("Screenshot sent to Report Portal")