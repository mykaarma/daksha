from .logs import *
from daksha import settings
from engine import models
from datetime import datetime

#This function initializes the test result of each YAML file in the database
def initialize_test_result(test_id,test_yml):
    time_now = datetime.now()
    processed_time_now = time_now.__str__().replace(":", "_")
    particular_test_result=models.ResultStored()
    if(settings.TEST_RESULT_DB != None and settings.TEST_RESULT_DB == "postgres"):
        logger.info(test_id)
        logger.info(test_yml["name"])
        logger.info("Initializing the entry in database of the abovestated test")
        particular_test_result.Test_Id=test_id
        particular_test_result.Test_Name=test_yml["name"]
        particular_test_result.Status="Waiting"
        particular_test_result.Failure_Cause="NULL"
        particular_test_result.Failure_Step="NULL"
        particular_test_result.InsertTs=processed_time_now
        particular_test_result.save()
        logger.info("Intialized the entry in database and will update when the test terminates")
    
    return particular_test_result
            