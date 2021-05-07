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

from daksha.settings import EMAIL_HOST_USER, POSTMARK_TOKEN, APACHE_URL, STORAGE_PATH
from .logs import *
from postmarker.core import PostmarkClient


def send_report_email(test_id, report_url, recipient_email):
    """
    Sends email to the recipient email provided
     :param test_id: ID of the Test
     :type test_id: str
     :param report_url: The url where the report is hoisted
     :type report_url: str
     :param recipient_email:  The email where the report will be sent
     :type recipient_email: str
    """

    subject = "Report for Test ID: " + test_id

    if len(APACHE_URL) == 0:
        test_folder = STORAGE_PATH + '/' + test_id + '/'
        message = "Please open this folder on your system to get the test Report : '" + test_folder + "'"
    else:
        folder_url = APACHE_URL + test_id + '/'
        message = "Please open this url to get your test Report : " + report_url + "\nTest folder url: " + folder_url
    # message.attach_file('/templates/testPage.html')
    logger.info(message)
    if len(POSTMARK_TOKEN) == 0:
        logger.info('Report not emailed, Postman token not set')
    else:
        send_email_postmark(subject, message, recipient_email)
        logger.info('Email sent to ' + recipient_email)


def send_email_postmark(subject, message, recipient_email):
    postmark = PostmarkClient(server_token=POSTMARK_TOKEN)
    postmark.emails.send(
        From=EMAIL_HOST_USER,
        To=recipient_email,
        Subject=subject,
        HtmlBody=message
    )
