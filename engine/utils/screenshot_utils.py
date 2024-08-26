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
import os
from datetime import datetime
from daksha.settings import STORAGE_PATH

def take_screenshot(test_uuid, test_name,  web_driver):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S.%f')[:-3]
    screenshot_dir = f"{STORAGE_PATH}/{test_uuid}/Screenshots/{test_name}"
    if not os.path.isdir(screenshot_dir):
        os.makedirs(screenshot_dir)
    screenshot_file = f"{screenshot_dir}/{current_time}.png"
    web_driver.save_screenshot(screenshot_file)
    with open(screenshot_file, "rb") as file:
            screenshot_data = file.read()
    return screenshot_data
