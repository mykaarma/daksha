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

from .selenium_helper import *
from .api_response import make_http_request

# this mapper maps the action allowed in the yml file to corresponding method that implemented it

# action: implementing_method

# Each of the methods listed here must take webdriver and test_uuid as params

method_map = {
    "config": browser_config,
    "launch_browser": launch_browser,
    "open_url": open_url,
    "fill_data": fill_data,
    "click_button": click_button,
    "select_in_dropdown": select_in_dropdown,
    "validate_ui_element": validate_ui_element,
    "quit_browser": quit_browser,
    "switch_iframe": switch_iframe,
    "switch_to_default_iframe": switch_to_default_iframe,
    "refresh_page": refresh_page,
    "navigate_back": navigate_back,
    "open_new_tab": open_new_tab,
    "switch_to_tab": switch_to_tab,
    "make_HTTP_request": make_http_request,
    "wait_for": wait_for,
    "capture_ui_element": capture_ui_element,
    "scroll_to": scroll_to,
    "download_file": download_file,
    "read_file":read_file,
}
