Daksha
===============================================

## Introduction
Daksha is a django framework based dynamic test case execution API.You can write any variation of UI-based test cases in a yml file and execute them right away with this new tool in town. <br /> For example: Sign in to any of your social media account and sign out or sign in then perform a task and then sign out. <br /> The API request should comprise of the location of the yml file.To summarize in simple terms the working can be divided into two steps -
* [Sending API Request](daksha_know-how/ApiRequest.md)
* [Writing Test Case](daksha_know-how/CreateTest.md)

You can also auto-generate test yamls through Daksha Recorder [chrome extension](recorder/extensions/chrome/ReadMe.md).

## Quickstart 
#### ⚠️ Warning (This is not compatible with ARM64 architecture.)

To run your first test case with Daksha, follow the steps in [QuickStart](daksha_know-how/QuickStart.md).

## Building and Running

### Using docker

  - Setup a local or remote chromedriver for your tests
  - Take a look at [docker-compose.yml](docker-compose.yml) file and create all the necessary [environment variables](#environment-variables).
  - Run the command `docker-compose up -d` to initiate the build and deploy the project.
  
  - NOTE: If you're running the application through docker and intend to run scripts saved locally, make sure to mount the location of test yamls to the container so that test yamls could be accessed from inside of container.

### Local deployment (without docker)

  - Download [python 3.8+](https://www.python.org/downloads/) and setup a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
  - Install all requirements using `pip install -r requirements.txt`
  - (Optional) Create any env variables needed.
  - Download Chromedriver (https://chromedriver.chromium.org/downloads)
  - Run `.\startup_command.bat` to start the project in case of Windows.
  - Run `sh startup_command.sh` to start the project in case of Linux.
  - Run `sh startup_command_mac.sh` to start the project in case of MacOS.

## Setting up webdriver
We only support chromedriver at this point.

### Local Webdriver
Download Chromedriver according to your chrome version from https://chromedriver.chromium.org/downloads. You can later refer this path from your test yml.

### Remote Webdriver
Setup selenium grid using https://www.selenium.dev/downloads/. Or if you want to use the dockerized version you can download and run selenium grid images from dockerhub: https://hub.docker.com/u/selenium.

## Database
 - The user can opt for this functionality if he/she wants to save the test results in the database.
 - To enable this, please provide the following environment variables:-
 `TEST_RESULT_DB`, `PG_DB`, `PG_USER`, `PG_PASSWORD`, `PG_HOST`, `PG_PORT`

 - We only support Postgresql database at this point. To enable this one has to set the environment        variable `TEST_RESULT_DB` to `postgres`.
 - This functionality is optional and Daksha workflow does not depend on it.

### Deploying Daksha with Database enabled by Docker
 - Run the command `docker-compose up -d` to initiate the build and deploy the project.

### Deploying Daksha with external Postgressql Database
 - This assumes that you have an external Postgresql database up and provide the correct environment variables :-
 `TEST_RESULT_DB`, `PG_DB`, `PG_USER`, `PG_PASSWORD`, `PG_HOST`, `PG_PORT`
 - Comment out the database service in [docker-compose file](./docker-compose.yml).
 - Run the command `docker-compose up -d` to initiate the build and deploy the project.

## Cron Jobs
 - The user can opt for this functionality if he/she wants to run tests at regulated intervals without hitting the api endpoints.
 - To enable this the user has to provide an environment variable `CRON_ENABLED` and set it to `true`.
 - If `CRON_ENABLED` is `true` then user has to provide additional environment variables `CRON_FILE_SOURCE`
 and `CRON_FILE_PATH`.
 - The user has to provide the description of Cron Jobs he/she wants to regulate in a YAML file. This yaml file can be loaded locally or from github. In both cases the necessary environment variables have to be set up accordingly.
 - Note that the YAML file containing cron jobs description and the YAML files containing the tests to be executed must not be present in same sub folders in the github branch.
 - The format of the yaml file containing the cron jobs description is provided in [CronJob Description](daksha_know-how/CronJobsDescription.md)

 - If the user is deploying the application locally, the CronJob functionality is only supported in Unix-like operating systems like Linux and macOS.
 - Windows users need to deploy the application using Docker to avail the CronJob functionality.

## Receiving Test Result Data 
- The user can recieve the test result data by providing TestUUID. 
- In order to utilize this functionality, the user must have chosen the database feature and configured the required environment variables.
- To receive the test result data, the user has to hit a GET request at the endpoint:-
  - `http://127.0.0.1:8083/daksha/tests/{testuuid}` if the application is deployed through docker.
  - `http://127.0.0.1:8000/daksha/tests/{testuuid}` if the application is deployed locally.
- The user has the option to retrieve test result data for all tests associated with a TestUUID or can specify the desired test name in the query parameters as :-
  - `http://127.0.0.1:8083/daksha/tests/{testuuid}?testName={testName}` if the application is deployed through docker.
  - `http://127.0.0.1:8000/daksha/tests/{testuuid}?testName={testName}` if the application is deployed locally.
- Different possibles responses are:-
  - Status Code 405 : Method not allowed
    - Please recheck that the method of the request is GET.
  - Status Code 400 : Bad Request
    - Please recheck that the TestUUID is entered correctly.
    - Please recheck that the Test Names provided in the query parameters are given correctly.
    - Please recheck that the database functionality is opted for and all the necessary environment variables are set.
  - Status Code 404 : Page not found
    - Please recheck that the correct endpoint is being hit.

## Report Portal
- Users can choose to integrate Daksha test reports with [Report Portal](https://github.com/reportportal).
- To enable this integration, users need to provide specific environment variables: 
`REPORT_PORTAL_ENABLED`, `REPORT_PORTAL_PROJECT_NAME`, `REPORT_PORTAL_ENDPOINT`, `REPORT_PORTAL_TOKEN`.
- To enable this functionality, set the value of `REPORT_PORTAL_ENABLED` to `True`.
- User must have deployed Report Portal through building the [Report Portal Docker Compose file](https://github.com/reportportal/reportportal/blob/master/docker-compose.yml). 
- The user can also use the same Postgres server for Report Portal and Daksha.To enable this, Please edit the [Report Portal Docker Compose file](https://github.com/reportportal/reportportal/blob/master/docker-compose.yml) and expose the ports of the Postgres Database before initiating the build.
- This can be done by uncommenting the ports section for postgres service defined in the yml file.
- Users must ensure that the Report Portal service is deployed and that the environment variable values align with the deployed service.
- Run the command `docker-compose up -d` to initiate the build and deploy the project.

## #Environment Variables
You can configure the application in a lot of ways by setting the following environment variables:
* **STORAGE_PATH**
  * This is the location of directory where reports generated by the application are stored.
  * Defaults to 'reports' in current directory.

* **APACHE_URL**
  * If you're using a hosting service (like apache) to host your reports, put the base URL here.
  * Make sure that this base url is mapped to whatever location the reports are stored. (governed by **STORAGE_PATH** environment variable)

* **LOG_FILE**
  * This is the location where reports generated by the application are stored.
  * Defaults to 'logs/uiengine.log' in current directory.

* **POSTMARK_TOKEN**
  * This is the postmark token which will be used to send reports by email.
  * If not set, we'll skip sending the email.
  
* **ALERT_URL**
  * This is the alert webhook url which will be used to send alerts in gchat/slack.
  * If not set, we'll skip sending the alert.
  
* **EMAIL_HOST_USER**
  * This is the email ID from which reports should be sent.

* **GIT_USER**
  * Github username for logging into github to fetch test yamls.
  * Don't set it/Leave it blank if the repo is public and no authentication is needed.

* **GIT_PASS**
  * Github password for logging into github to fetch test yamls.
  * Don't set it/Leave it blank if the repo is public and no authentication is needed.

* **REPO_USER**
  * Name of user who owns the github repository containing the test yamls.
  * Only one of the variables **REPO_USER** and **REPO_ORG** should be set at a time.

* **REPO_ORG**
  * Name of organization which owns the github repository containing the test yamls.
  * Only one of the variables **REPO_USER** and **REPO_ORG** should be set at a time.

* **REPO_NAME**
  * Name of the github repository containing the test yamls.

* **BRANCH_NAME**
  * Name of the branch containing the test yamls in the github repository defined by **REPO_NAME**.

* **DJANGO_SECRET_KEY**
  * Use this variable if you want to override the default value of SECRET_KEY for added security.

* **ALLOWED_HOSTS**
  * Provide a comma separated list of hosts which you'd like to be added to ALLOWED_HOSTS.

* **TEST_RESULT_DB**
  * If you want to use the Postgresql database to save your test reports, create this environment variable and set its value to `postgres`.
  * If you set this value as `postgres`, you need to provide additional environment variables.
  * If you don't want the database functionality, delete this environment variable or set it to disabled.

* **PG_DB**
  * Name of the database. If this value is not provided, the default name of database will be `postgres`.

* **PG_USER**
  * Name of the User. If this value is not provided, the default name of user will be `postgres`.

* **PG_PASSWORD**
  * Password corresponding to the user. Default password for user postgres is `postgres`.

* **PG_HOST**
  * The host of our database. If this value is not provided, the default host is `localhost`.

* **PG_PORT**
  * Port provided to the database. If this value is not provided, the default port will be `5432`.

* **CRON_ENABLED**
  * If you want to run tests at regulated intervals, set this variable to `true`.
  * If you don't want to run cron jobs, delete this environment variable or set it to `false`.

* **CRON_FILE_SOURCE**
  * This value can either be `local` or `git`. It denotes the source of yaml file which contains Cron jobs description.

* **CRON_FILE_PATH**
  * This value should be set to the path of the yaml file which contains cron job description.

* **REPORT_PORTAL_ENABLED**
  * This value should be set to `True` if the user wants the Test reports to be displayed in Report Portal.

* **REPORT_PORTAL_ENDPOINT**
  * This value should be set to the URL of the ReportPortal server where the client should connect to.

* **REPORT_PORTAL_PROJECT_NAME**
  * This values should be set to the name of the specific project or workspace within ReportPortal where the user wants to show the Daksha test reports.

* **REPORT_PORTAL_TOKEN**
  * This value should match the authentication token provided by the user-deployed ReportPortal.Please refer [Token to be used by Report Portal Client Tools](https://reportportal.io/docs/reportportal-configuration/HowToGetAnAccessTokenInReportPortal/#2-authorization-with-users-uuid-access-token-for-agents)

## Get in Touch

* Open an issue at: https://github.com/mykaarma/daksha/issues
* Email us at: opensource@mykaarma.com

## Contributions

We welcome contributions to Daksha. Please see our [contribution guide](CONTRIBUTING.md) for more details.

## License
Copyright 2021 myKaarma

Licensed under the [GNU Affero General Public License v3](LICENSE)

## Motivation

[Information Modal](https://github.com/mykaarma/information-modal)
