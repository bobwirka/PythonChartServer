# Python Chart Server

Version 1.0 : 1-Jan-2018

Example Python project that illustrates a chart server.

This project uses Chart.js to display the charts.

Client side code is written in TypeScript.

Right now, the chart data is incorporated in each chart's JSON file. There are provisions
in the works to update the data after the chart has been loaded so that changing data can
be displayed dynamically. Just haven't written the Python part...

Have added 'start.sh' script that will start the server and open a google chrome window that will
be resized when the application starts. Substitute chromium-browser for google-chrome-stable if
you're using chromium.

**BONUS FEATURE**

Added window resize to 'client/index.ts' so that if the browser is started as a new window in
application mode, the window will become smaller to fit the user interface. There will be no
tabs, bookmarks, etc.

Yes, it's then a Web App...

You can start Chrome or chromium or Chrome from the command line to do this:
```sh
google-chrome-stable --new-window --app=http://localhost:8080/index.html
    --OR--
chromium-browser --new-window --app=http://localhost:8080/index.html
```
