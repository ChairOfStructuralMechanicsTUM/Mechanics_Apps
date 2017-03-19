# Server Architecture

We provide access to the apps through a bokeh server in directory format (see http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#directory-format). Our overview website is hosted by a nginx server which forwards requests to the bokeh server.

The server can be run in two modes:

* [x] online mode: provide access to apps through the internet.
* [x] offline mode: run the server locally and present apps to
lecture audience.

## ToDos

- [x] works on Linux?
- [x] works on Windows?
- [x] works on MacOS?
- [x] create installer scripts automatically performing setup (lecturers can easily install framework on their machines)
- [ ] test setup online mode on webserver
