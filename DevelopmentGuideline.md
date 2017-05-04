# Coding Style

* for directory names use ```_``` for blank space. In the app title (see formatting hints below) use a real blank. **do not use ```-```**

# Developer Workflow

The following points are important for all developers.

* Apps that are not executable using ```bokeh serve --show app_directory``` should **not** be pushed to master, you may use a branch for experimental apps.
* Develop app in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format).
* Use the **same** name for the directory and the title of the app. Language depends on the language of the lecture. See also coding style above.
* If your app is completed ask your supervisor whether there are any additional improvements to be done or if the app is ready for publication.
* Write a mail to Francesca that your app is ready for publication.

# Francesca Final Acceptance and Publication

The following points are executed by Francesca only.

* Make sure that the status of finalized apps is updated in ```Mechanic_Apps/README.md``` (done by Francesca)
* Add description of app and a matching tooltip on overview page
    * put app in the right position in the hierarchy (semester, lecture).
* Add app directory name to ```appnames.conf```.
    * Maintain alphabetical order.
* Test setup by starting the server locally (```Mechanic_Apps.exe```):
    * Is the app working?
    * Can you access the app from the overview page?
* Publish new app to server:
    * Push to master branch from local machine
    * Pull from git on server
    * Relauch server using ```server_autorun.exe```.

# Formatting hints

* use ```curdoc().title = "Appname"``` for defining the title. This title can be seen, for example in the Tab title of the browser.
