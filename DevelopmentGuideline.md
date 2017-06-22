# Coding Style

* for directory names use ```_``` for blank space. In the app title (see formatting hints below) use a real blank. **do not use ```-``` or CamelCase style**

# Developer Workflow

The following points are important for all developers.

* Apps that are not executable using ```bokeh serve --show app_directory``` should **not** be pushed to master, you may use a branch for experimental apps.
* Develop app in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format).
* Use the **same** name for the directory and the title of the app. The title of the app shall explain the mechanical content - not the method of visualization. (e.g. use "conservation of momentum" instead of "boat with three swimmers"). See also coding style above.
* Lanuage: The Language of everything (titles, explanations, comments in code, etc.) within the whole project is **English**!
* Avoid global variable! 
* For the description file, formulas can be added with the aid of MathJax http://docs.mathjax.org/en/latest/start.html
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

* We use ```curdoc().title = "Appname"``` for defining the title. This title can be seen, for example in the Tab title of the browser. Your directory name should comply with the standard defined above. Use

    ```
    curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')
    ```

    This gets path of parent directory and only uses the name of the Parent Directory for the app title name. Then it replaces underscores '_' and minuses '-' with blanks ' '.
