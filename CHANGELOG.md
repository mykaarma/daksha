# `DAKSHA` Change Log

*version*: `2.10.0`

## v 2.10.0
1. Added Report Portal functionality to display Daksha Test Reports.

## v 2.9.0
1. Modified GET endpoint to include test name as query params. 

## v 2.8.0
1. Added startup_command.bat for starting the app locally in Windows. 

## v 2.7.0
1. Added the Variable Dictionary in the test result table of postgres database. 
2. Changed request method to retrieve data to POST.

## v 2.6.1
1. Started the server using gunicorn.

## v 2.6.0
1. Added startup command in entrypoint.
   
## v 2.5.0
1. Added minor imporvement in startup command for db.
   
## v 2.4.1
1. Modified permissions and fixed initialisation issues with cron jobs.

## v 2.4.0
1. Created a GET endpoint to recieve test result data by providing TestUUID.

## v 2.3.0
1. Added Cron Job functionality to run tests in regulated intervals.

## v 2.2.2
1. Fixed server initialisation issue in case of running daksha server in local with no database.

## v 2.2.1
1. Added In_Progress status for tests in database.

## v 2.2.0
1. Added Database for Test Results in Daksha.
2. Users can opt for test results to be saved in a Postgres database.

## v 2.1.3
1. Adressed issue #47

## v 2.1.2
1. Added UI functionality to Daksha Chrome Extension.

## v 1.1.0
1. Added chrome extension for autogenerating Daksha Yaml

## v 1.0.1
1. Added scroll_to functionality in helper methods

## v 1.0.0
1. Adressed issues #11 , #15 , #19 , #29

## v 0.3.2
1. Changed python version to 3.10 in Dockerfile

## v 0.3.1
1. Fixed dependabot alerts

## v 0.3.0
1. Added Alert Sending feature on test failure

## v 0.2.2
1. Fixed open_new_tab method

## v 0.2.1
1. Added wait method
2. Fixed switch_iframe method

## v 0.2.0
1. Added API call functionality

## v 0.1.0
1. Added variable support in yaml
2. Added variable_dictionary to engine

## v 0.0.1
1. Initial release