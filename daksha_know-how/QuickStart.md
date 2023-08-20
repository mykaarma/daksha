# Quick Start

Welcome to Daksha! This quick start guide will walk you through the process of running your first testcase using Daksha. Follow these three main steps to get started:

1. Run the Daksha Server.
2. Create a `test.yml` using the Daksha Recorder.
3. Send an API request to Daksha.

## Using Docker (Recommended for Users)

### Run Daksha Server

   - Open your terminal or command prompt based on your operating system.
   - Clone the [Daksha Repository](https://github.com/mykaarma/daksha):
     
      ```git clone https://github.com/mykaarma/daksha.git```
   - Navigate to the directory where you cloned Daksha and open a terminal here.
   ```cd daksha```
   - Install Docker Desktop. Refer [Docker Documentation](https://docs.docker.com/compose/install/)
   - Start the Docker engine.
   - Create a test-data directory.
   ```mkdir test-data```
   - Inside the test-data directory create a db-data directory. The database files will reside in this directory.
   ```mkdir test-data/db-data```
   - Run the command `docker-compose up -d` to initiate the build and deploy the project.
      For macOS the command will be `docker compose up -d`.
   - You now have the daksha server running.

### Create a test YAML file using the Daksha Recorder

   - Open chrome web store and add [Daksha Recorder Extension](https://chrome.google.com/webstore/detail/daksha-recorder/gmpmpceenkghjdlelhgepnknlijllfom?utm_source=ext_sidebar&hl=en-GB) to your chrome.
   - Please refer to this [video recording](https://youtu.be/4FRdS2iJZoQ?t=986) for creating a test.yml using Daksha Recorder.
   - Download the test YAML (HelloWorld.yml) from Daksha Recorder.
   - The following configs are user specific , so the recorder keeps them empty.You will need to edit the downloaded YAML file to add the following values.
   ```
   config:
     env: local
     browser: chrome
     driverAddress: http://selenium-hub:4444/wd/hub
   name: HelloWorld
   ```
   Here is an exapmle test YAML file-  HelloWorld.yml
   - Move this file to the `test-data` directory created in previous step.

### Hit API Request

   - Copy the following curl request. Replace the email field and path field in the curl. Path should be /test-data/{your file name}. This is the path of the test.yml that you had copied in the test-data directory and mounted in docker.
   ```curl --location --request POST 'http://127.0.0.1:8083/daksha/runner' \
--header 'Content-Type: text/plain' \
--data-raw '{
         "email": "your.email@mykaarma.com",
         "test": {
         "source": "local",
         "type": "file",
         "path": "/test-data/HelloWorld.yml",
         "variables": ""
         }
      }'```

### See what is happening inside the test

   - Open this url http://localhost:4444/ui#/sessions 
   - In sessions you will see active session being generated on hitting the API request.
   - Click on the video icon and enter password `secret`. You will be able to see what the steps being executed in chrome.
