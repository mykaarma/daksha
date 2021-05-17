# Daksha Api Request
You can host the API in your local server or at a central server and then hit an API request. You should hit the API request to the URL- ***http://{IP}:{port}/engine/singletest***. For local the port is 8000  and for a central server the port is 8083.
The API request body consists of the following fields-
  * **email**-This is the email Id to which the execution status report would be send.
  * **fileLocation**- You can either load your test case file from local device or from github repository.Depending on your choice it may have either of the 2 values: local or git.
  * **file**-This is the location of your test case file(yml format).
  Example-
     
```		
    curl --location --request POST 'http://127.0.0.1:8083/engine/singletest' \
    --header 'Content-Type: text/plain' \
    --data-raw '{
       "email": "your_email@mykaarma.com",
       "fileLocation": "git",
       "file": "folder/mytest.yml"
                }' ```
        
	
