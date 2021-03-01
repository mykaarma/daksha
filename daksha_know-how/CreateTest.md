# Writing Your First Test Case with Daksha

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
name:TestQA
task:
  - launch_browser
  - open_url:
      url: https://app.mykaarma.com
  - fill_data:
      xpath: //*[@id='firstPhaseInputs']//input[@placeholder='Username'] 
      value: ab@mykaarma
  - click_button:
      xpath: //*[@id='bSignIn']
  - fill_data:
      xpath: //*[@id='password']
      value: @NoSoupForYou
  - click_button:
      xpath: //*[@id='bchromedriverSignIn']
  - validate_ui_element:
      mode: equals
      xpath: //div[@class='headertoprightDealerName']
      value: myKaarma
  - click_button:
      xpath: //*[text()='Sign Out']

  - quit_browser 
  ```

  
 * **config**-This should contain the browser configurations. It has three fields namely env,browser,driverAddress. 
   * **env**-It may have two values- remote or local. For witnessing your tests being executed in your device,you can set this to local and then give the browser details in the next 2 fileds. Similarly if you want your test to be executed at a remote browser you can set this to remote.Users can use a VNC client to see the tests being executed in remote browser.
   * **browser**-Currently we are supporting chrome only, so the value should be chrome.
   * **driverAddress**-You can either give location of your local chrome browser or the url at which your remote chrome browser is hosted.
 * **name**- Give a name to your testcase.This will be dispayed in your test report.
 * **task**- This will contain the steps of your test.For writing this section please take a look at the list of functionalities that we are providing in the below list.You can perform simple to complex test cases with a combination of the below functionalities.
   * ***launch_browser***: This will launch the browser in the environment and location provided in the config field.You should always include this step in the start of your test case steps.
   * ***open_url***: Provide the url of the site that you want to perform tests on.
   * ***fill_data***: This has two sub-fields,namely *locator* and *value* . **Locator** can be *xpath, id, css, name, tagname, classname, linktext and partiallinktext*. In **locator** you should provide the type of locator you are providing followed by the  webelement where you want to fill the data and in the *value* field provide the data that you want to enter.
   * ***click_button***: You need to provide the locator of the webelement that you want to click.
   * ***validate_ui_element***: This has 3 field: *mode, locator, value*.In *mode* you can select 3 types of validation method namely **equals,contains and not contains**.In *locator* give the locator of your webelement and in *value* give the text with which you want to validate.
   * **refresh_page**: This can be added to refresh the webpage.
   * **open_new_tab**: This will open a new tab in your browser.
   * **switch_to_tab**: Here the title of the tab to which you want to move to needs to be provided as a subfield.
   * **navigate_back**: This can be used to go back to previous page.
   * **switch_iframe**:  Here you need to provide the **locator** as a subfield and it will switch to that iframe.
   * **switch_to_default_iframe**: This will take you to the default frame.
   * **quit_browser**: You are recommended to add this step at the end of your test case steps to quit the remote or local browser.
   



 
  
