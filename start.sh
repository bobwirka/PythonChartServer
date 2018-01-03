#!/bin/bash
#
# Starup script that loads the server and starts chrome in application mode.
# The app.js code resizes the window to better fit the UI.
#
server/app.py &
google-chrome-stable --new-window --app=http://localhost:8080/index.html &
