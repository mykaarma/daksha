# Description of Cron Jobs 

You need to write test case in yml file and it should be in the following format -
```
crons: 
- cron: 
  params:
    email: 
    test:
      source: 
      type: 
      path: 
      variables: 

   ```
A complete test case example is given below along with the description of each field and functionality that we are supporting:

```		
crons: 
- cron: "*/2 * * * *"
  params:
    email: abc.123@gmail.com
    test:
      source: git
      type: file
      path: examples/loginlogout.yml
      variables:
        username: ab@mykaarma
        password: "@NoSoupForYou"
- cron: "*/3 * * * *"
  params:
    email: efg.456@mykaarma.com
    test:
      source: local
      type: file
      path: examples/sendtext.yml
      variables:
        username: ab@mykaarma
        password: "@NoSoupForYou"

                ' 
```

* **crons**
   * **cron**-This is the expression defining intervals at which our test will be regulary executed.
   * **params**
        * **email**- This is the email Id to which the execution status report would be send.
        * **test**- This will contain the details of test to be executed
            * **source**- You can either load your test case file from local device or from github repository.Depending on your choice it may have either of the 2 values: local or git.
            * **type**- This is the type of source, i.e. file/folder
            * **path**- This is the location of your test case file(yml format).
            * **variables**- This is the dictionary containing the variables to be rendered in the yml file.

   