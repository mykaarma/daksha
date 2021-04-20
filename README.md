Daksha
===============================================

## Introduction
Daksha is a django framework based dynamic test case execution API.You can write any variation of UI-based test cases in a yml file and execute them right away with this new tool in town. <br /> For example: Sign in to any of your social media account and sign out or sign in then perform a task and then sign out. <br /> The API request should comprise of the location of the yml file.To summarize in simple terms the working can be divided into two steps -
* [Sending API Request](daksha_know-how/ApiRequest.md)
* [Writing Test Case](daksha_know-how/CreateTest.md)

## Building and Running

### Using docker

  - Take a look at [docker-compose.yml](docker-compose.yml) file and create all the necessary environment variables.

  - Run the command `docker-compose up -d` to initiate the build and deploy the project.

### Local deployment (without docker)

  - Create a virtual environment using python 3.7
  - Install all requirements using pip install -r requirements.txt
  - Create any env variables needed
  - Run `python manage.py runserver` to start the project

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
