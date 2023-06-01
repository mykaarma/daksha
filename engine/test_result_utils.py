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
from daksha import settings
from engine import models

def initialize_test_result(test_id,test_yml):
    test_result=models.TestResults()
    if(settings.TEST_RESULT_DB != None and settings.TEST_RESULT_DB.lower() == "postgres"):
        test_name=test_yml["name"]
        test_result.TestUUID=test_id
        test_result.TestName=test_name
        test_result.Status="Waiting"
        test_result.save()
        logger.info(f"Initialized test named {test_name} with TestUUID {test_id} in the database")
        
    else :
        logger.info("The Test results would not be saved in database as that functionality is not opted for")
    return test_result
            
            
def save_result_in_db(test_executor,execution_result,step,error_stack):
    test_name=test_executor.test_yml["name"]
    testUUID=test_executor.test_id
    if execution_result:
        test_executor.test_result.Status="Passed"
    else:
        test_executor.test_result.FailureStep=str(step)[0:200]
        test_executor.test_result.FailureCause=str(error_stack)[0:200]
        test_executor.test_result.Status="Failed"
                
    test_executor.test_result.save()
    logger.info(f"The Test Result for test named {test_name} of TestUUId {testUUID} have been updated in the database")