# Quick Start

## Building and Running

### Using docker

  - Install Docker and the Compose plugin. Refer [Docker Documentation](https://docs.docker.com/compose/install/)
  - Start the Docker engine. This can be done by running the command ```docker``` in the terminal.
  - Setup a local or remote chromedriver for your tests
  - Clone the [Daksha Repository](https://github.com/mykaarma/daksha)
  - Take a look at [docker-compose.yml](../docker-compose.yml) file and create all the necessary [environment variables](../README.md#environment-variables).
  - Navigate inside the directory where you cloned Daksha and open a terminal here.
  - Run the command `docker-compose up -d` to initiate the build and deploy the project.

### Local Deployment (without Docker)

  - Clone the [Daksha Repository](https://github.com/mykaarma/daksha)
  - Navigate to the directory where you cloned Daksha and open a terminal here.
  - Download [python 3.8+](https://www.python.org/downloads/) and setup a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
  - Install all requirements using `pip install -r requirements.txt`
  - Create all the necessary [environment variables](../README.md#environment-variables).
  - Download [Chromedriver](https://chromedriver.chromium.org/downloads)
  - Run `.\startup_command.bat` to start the project in case of Windows.
  - Run `sh startup_command.sh` to start the project in case of Linux.
  - Run `bash startup_command_mac.sh` to start the project in case of MacOS.

## Run your first test
   - Refer [CreateTest](./CreateTest.md) and provide the necessary values in [HelloWorld.yml](./HelloWorld.yml).

### Test YAML loaded from local storage and Daksha deployed locally (without Docker)
   - To run your first test, copy the absolute path of [HelloWorld.yml](./HelloWorld.yml) and supply this value in API request as mentioned below.
   - Hit the API request by importing the following curl command in Postman: 
   ```		
      curl --location --request POST 'http://127.0.0.1:8000/daksha/runner' \
      --header 'Content-Type: text/plain' \
      --data-raw '{
         "email": "your.email@mykaarma.com",
         "test": {
         "source": "local",
         "type": "file",
         "path": "{absolute path of YAML test file}",
         "variables": ""
         }
      }'
   ```
### Test YAML loaded from GitHub and Daksha deployed locally (without Docker)
   - Upload/Create [HelloWorld.yml](./HelloWorld.yml) in your GitHub repository and provide the necessary environment varaibles
   - Provide the path of [HelloWorld.yml](./HelloWorld.yml) relative to GitHub repository structure in the API request
   - Hit the API request by importing the following curl command in Postman: 
   ```		
      curl --location --request POST 'http://127.0.0.1:8000/daksha/runner' \
      --header 'Content-Type: text/plain' \
      --data-raw '{
         "email": "your.email@mykaarma.com",
         "test": {
         "source": "git",
         "type": "file",
         "path": "{path of YAML test file relative to GitHub repository structure}",
         "variables": ""
         }
      }'
   ```
### Test YAML loaded from local storage relative to Docker Container and Daksha deployed through Docker
   - Mount [HelloWorld.yml](./HelloWorld.yml) into the container so that it could be accessed from inside of container.
   - To run your first test, copy the path of [HelloWorld.yml](./HelloWorld.yml) in your Docker Container and supply this value in API request as mentioned below.
   - Hit the API request by importing the following curl command in Postman: 
   ```		
      curl --location --request POST 'http://127.0.0.1:8083/daksha/runner' \
      --header 'Content-Type: text/plain' \
      --data-raw '{
         "email": "your.email@mykaarma.com",
         "test": {
         "source": "local",
         "type": "file",
         "path": "{path of YAML test file in your Docker Container}",
         "variables": ""
         }
      }'
   ```

### Test YAML loaded from GitHub and Daksha deployed through Docker
   - Upload/Create [HelloWorld.yml](./HelloWorld.yml) in your GitHub repository and provide the necessary environment varaibles
   - Provide the path of [HelloWorld.yml](./HelloWorld.yml) relative to GitHub repository structure in the API request
   - Hit the API request by importing the following curl command in Postman:
   ```		
      curl --location --request POST 'http://127.0.0.1:8083/daksha/runner' \
      --header 'Content-Type: text/plain' \
      --data-raw '{
         "email": "your.email@mykaarma.com",
         "test": {
         "source": "git",
         "type": "file",
         "path": "{path of YAML test file relative to GitHub repository structure}",
         "variables": ""
         }
      }'
   ```
