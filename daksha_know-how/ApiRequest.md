# Daksha Api Request
You can host the API in your local server or at a central server and then hit an API request. You should hit the API request to the URL- ***http://{IP}:{port}/engine/singletest***. For local the port is 8000  and for a central server the port is 8083.
The API request body consists of the following fields-
  * **email**-This is the email Id to which the execution status report would be send.
  * **test**- This will contain the details of test to be executed
    * **source**- You can either load your test case file from local device or from github repository.Depending on your choice it may have either of the 2 values: local or git.
    * **type**- This is the type of source, i.e. file/folder. Note that the folder containing test case yml files should not contain any yml files which is not a test case yml file / does not follow the test case yml format
    * **path**- This is the location of your test case file(yml format).
    * **variales**- This is the dictionary containing the variables to be rendered in the yml file.

  Example-
     
```		
    curl --location --request POST 'http://127.0.0.1:8083/daksha/runner' \
    --header 'Content-Type: text/plain' \
    --data-raw '{
       "email": "your.email@mykaarma.com",
       "test": {
        "source": "local",
        "type": "folder",
        "path": "/Users/Documents/daksha/examples",
        "variables" : {
           "username" : "ab@mykaarma",
           "password" : "@NoSoupForYou"
        }
      }
   }
                ' 
```
