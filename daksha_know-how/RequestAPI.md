# Making API calls with Daksha

You need to write test case in yml file and it should be in the following format -
```config:
   name:
   task:
   ```
A complete test case example is given below along with the description of each field and functionality that we are supporting:

```
config:
  env: remote
  browser: chrome
  #driverAddress: /Users/IdeaProjects/qa-automation/ui_automation_engine/drivers/chromedriver
  driverAddress: http://192.168.21.185:4444/wd/hub
name:APISupportTest
task:
  - make_HTTP_request:
      request: 'POST'
      url : 'https://fakerestapi.azurewebsites.net/api/v1/Activities'
      headers : 
        accept: text/plain; v=1.0
        Content-Type: application/json; v=1.0
      data: '
        {
          "id": 0,
          "title": "string",
          "dueDate": "2021-06-23T18:03:18.689Z",
          "completed": true
        }'
      response:
        'status' : 200  #first check the response and then we will move ahead
        save:          #user need to pass this save key and the values must be passed as lists
          - 'key' : "title"
            'save in' : title
  - make_HTTP_request:
      request : 'GET'
      url : 'https://httpbin.org/basic-auth/{{username}}/{{passwd}}'
      headers: 
        accept : 'application/json'
      auth: 
        type : "Basic" #can be Basic, Digest and Proxy
        username : "{{ username}}"
        password : "{{ passwd }}"
      Cookies:
        custom_cookie : 
          'cookie_name': 'cookie_value'
      timeout: 12  #it can be integer or tuple
      response: 
        'status' : 200  #after making the http request, first check the response and then we will move ahead
        save:          #user need to pass this save key and the values must be passed as lists
          - 'save in' : response_get_body
  - make_HTTP_request:
      request: 'PUT'
      url : 'https://fakerestapi.azurewebsites.net/api/v1/Activities/{{id}}'
      headers : 
        accept: text/plain; v=1.0
        Content-Type: application/json; v=1.0
      payload: '{
        "id": 1,
        "title": "string",
        "dueDate": "2021-06-14T03:56:36.635Z",
        "completed": true
      }'
      # response:
        # 'status' : 200 #no status code provided
  - make_HTTP_request:
      request: 'POST'
      url : 'https://httpbin.org/post'
      headers : 
        'accept' : 'application/json'
      data: >
        {
        "form": {
            "comments": "fast", 
            "custemail": "rg@gmail.com", 
            "custname": "Rg", 
            "custtel": "783849", 
            "delivery": "18:30", 
            "size": "medium", 
            "topping": [
              "cheese", 
              "onion", 
              "mushroom"
            ]
          }
        }
      response:
        'status' : 200  #after making the http request, first check the response and then we will move ahead
  - make_HTTP_request:
      request: 'DELETE'
      url : 'https://httpbin.org/delete'
      headers : 
        'accept' : 'application/json'
      response:
        'status' : 201 #status mismatch
        save:          #user need to pass this save key and the values must be passed as lists
          - 'save in' : response_delete_body
```

 * **config**-This should contain the browser configurations. It has three fields namely env,browser,driverAddress. 
   * **env**-It may have two values- remote or local. For witnessing your tests being executed in your device,you can set this to local and then give the browser details in the next 2 fileds. Similarly if you want your test to be executed at a remote browser you can set this to remote.Users can use a VNC client to see the tests being executed in remote browser.
   * **browser**-Currently we are supporting chrome only, so the value should be chrome.
   * **driverAddress**-You can either give location of your local chrome browser or the url at which your remote chrome browser is hosted.
 * **name**- Give a name to your testcase.This will be dispayed in your test report.
 * **task**- This will contain the steps of your test.For writing this section please take a look at the list of functionalities that we are providing in the below list.You can perform simple to complex test cases with a combination of the below functionalities.Only single task parameter is supported at a time.
   * **make_HTTP_request**- This will make the corresponding *HTTP* request to perform the CRUD operation.
    * **request**- User needs to Specify the type of request [GET,POST,PUT,DELETE] that they want to request.
    * **url**- Parameter of the request module to provide the url of the site that you want to request.
    * **headers**- Parameter of the request module to provide the headers.
          * The user can specify the ***accept*** key, to inform the server the type of content understandable by the user. If the ***accept*** header is not present in the request, then the server assumes that the client accepts all types of media.
          * The user can provide the ***Content-Type*** of the content that the will be returned from the server. *Optional key* 
          * The user can provide ***Authorization*** with the *Basic*, *Bearer* and other authorizations and the *Tokens*. These *Tokens* can also be parameterized. *Optional key*
          * Many other details like *Cookies*, *Caches* etc can be provided in the **headers**.
          * Providing the details in **''** is optional.
    * **payload**- Parameter of the *GET* request. The user can provide the data using this key.
    * **data**- Parameter of the *POST*, *PUT* and *DELETE*
    * **json** - User can provide the *json* data for all the supported requests. 
      User can either use *data*/*payload* or *json* while making the request.
      * While passing data through **payload**, **data** or **json**, user can either use *''* or *>* to provide the json data. 
        * While using *''* user cannot use *''* inside the content provided, while he/she shouldnot worry about the indentation.
        * While using *>* user can provide the data containing *''* but he/she need to maintain the proper indentation of the data provided.
    * **auth**- User need to specify the ***type*** of authentication [Basic,Digest,Proxy], ***username*** and ***password***.*Optional Parameter*. 
      * *Basic* will use *HTTPBasicAuth* auth token of the request module.
      * *Digest* will use *HTTPDigestAuth* auth token of the request module.
      * *Proxy* will use *HTTPProxyAuth* auth token of the request module.
      * User should use variable rendering functionality to pass username and password *recommended*
    * **Cookies**- User can send the cookies while making the request. User can provide the **custom-cookies**.*Optional Parameter*
    * **timeout**- Response will awaited till this time and *timeout exception* will be raised when exceeded.It can be either integer or tuple. *Optional Parameter*
    * **response**- This section will save the response received from the api call. 
      * User can specify the **status** that he wants to receive [2xx,3xx,4xx,5xx]. If the *status* doesn't match it will return *Status_mismatch* error. *Optional parameter*
      * If the user does not provide the **status**, it will work for 2xx,3xx and will throw error for 4xx and above *status_code*.
      * The main function of this key is to **save** the response recevied, and use it further.
      * **save**- The user needs to provide the key **save_in**, the vairable where the response must be saved. This key can be used further. *Optional parameter*
        * The user can fetch the response data from the *nested json*. This must be provided in **key**.  
          * If the response is nested dictionary then user can follow *parent_dict.child_dict.key*.
          * If the response has list in *parent_dict*, and the user want to access the ith dictionary key-value pair *parent_dict[i].key*
          * For further assistance, please read the **Jmespath** official documentation.
          * *Otional parameter*