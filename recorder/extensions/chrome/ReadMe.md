Daksha Recorder
===============================================

## Introduction
 Daksha Recorder is a chrome Extension based on javascript. It is used to record live user actions and create a YAML file which can used in [Daksha](https://github.com/mykaarma/daksha). This tool reduces the time consumed in creating the yml file and makes the process hassle free.User can download the yaml in his local and change the default config values to use in [Daksha](https://github.com/mykaarma/daksha).

## Create a test YAML file using the Daksha Recorder

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
     
## Building(For Development)
  This extension is published in chrome web store, however if you want to make some tweaks to the extension, you can follow the below guidelines
  - Clone the repository in your local environment
  - Extract all files
  - Install [Node.js](https://nodejs.org/en/download/)
  - In any terminal, open the folder with name "ChromeExtension" which is present in the extracted folder
  - In Terminal, Write following commands:
       * npm install
       * npm start
## Running
  - In google chrome, visit [chrome Extensions](chrome://extensions/)
  - Enable Developer Mode
  - click on Load Unpacked Button
  - Select the folder with name "ChromeExtension" which is repesent in cloned repo.
  - Enable the Extension and you are good to go ahead.
## Configuration Variables in Yml file
To know about these variables, you can refer [How-to-set-variables](https://github.com/mykaarma/daksha/blob/main/daksha_know-how/CreateTest.md)
