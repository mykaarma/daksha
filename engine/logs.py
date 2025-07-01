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
import threading

from reportportal_client.helpers import timestamp  # type: ignore
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

class ReportPortalLoggingHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.thread_local = threading.local()

        def set_service(self, service):
            self.thread_local.service = service

        def clear_service(self):
            if hasattr(self.thread_local, 'service'):
                del self.thread_local.service
        
        def set_item_id(self, item_id):
            self.thread_local.item_id = item_id

        def clear_item_id(self):
            if hasattr(self.thread_local, 'item_id'):
                del self.thread_local.item_id

        def emit(self, record):
            report_portal_service = getattr(self.thread_local, 'service', None)
            
            item_id = getattr(self.thread_local, 'item_id', None)
            
            if report_portal_service is not None and item_id is not None:
                msg = self.format(record)
                level = record.levelname
                if level == "WARNING":
                    level = "WARN"

                screenshot = record.__dict__.get('screenshot')
                if screenshot:
                    attachment = {"data": screenshot, "mime": "image/png"}
                    report_portal_service.log(
                        time=timestamp(),
                        message=msg,
                        level=level,
                        item_id=item_id,
                        attachment=attachment
                    )
                else:
                    report_portal_service.log(
                        time=timestamp(),
                        message=msg,
                        level=level,
                        item_id=item_id
                    )



def get_logger(service, item_id) -> logging.Logger:
    try:
        logger.info(f"Getting logger for {item_id}")
        child_logger = logging.getLogger(item_id)
        logFormatter = logging.Formatter('%(asctime)s [%(levelname)-7.7s]  %(message)s')
        child_logger.setLevel(logging.INFO)
        
        fileHandler = logging.FileHandler(LOG_FILE)
        fileHandler.setFormatter(logFormatter)
        child_logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        child_logger.addHandler(consoleHandler)
        logger.info(f"Logger created for {item_id}")
        if (
            REPORT_PORTAL_ENABLED is not None
            and REPORT_PORTAL_ENABLED.lower() == "true"
        ):
            report_portal_logging_handler = make_report_portal_handler(service, item_id)
            child_logger.addHandler(report_portal_logging_handler)
            logger.info(f"Report portal logging handler added for {item_id}")
    except Exception as e:
            logger.error("Exception occurred while getting logger", e)
            return logger
    return child_logger


def make_report_portal_handler(service, item_id=None):
   try:
    handler = ReportPortalLoggingHandler()
    handler.set_service(service)
    if item_id is not None:
        handler.set_item_id(item_id)
        return handler
   except Exception as e:
        logger.error("Exception occurred while making report portal handler", e)
   return handler

