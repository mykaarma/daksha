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
from .logs import *

def gchat_alert(test_id, name, step, error_stack):
    logger.info("Data filled successfully")
    return


switcher = {
    "gchat": gchat_alert
}


def send_alert(test_id, name, step, error_stack, alert_channel_type):
    # Get the function from switcher dictionary
    func = switcher.get(alert_channel_type, "no_alert")
    # Execute the function
    if (alert_channel_type == None) or (len(alert_channel_type) == 0):
        return
    else:
        return func(test_id, name, step, error_stack)
