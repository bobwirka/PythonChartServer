#!/usr/bin/python3
#
import os
import fnmatch
import pathlib
from http.server import BaseHTTPRequestHandler,HTTPServer
import json

# Assume we start from the root level.
client_path = 'client/'
chart_path = 'charts/'

mime_types = [
    'html',
    'js',
    'css',
    'ts',
    'map',
    'json',
    'ico',
    'png'
]

###############################################################
#
# The following functions are custom code, tailored to the
# particular application.
#
# In practice, they will be imported from a separate module.
#
###############################################################


def handle_post_request(post_json):

    """Passed object decoded from JSON request"""

    # This function would handle any POST requests.
    # It returns an object that will be JSON encoded and
    # returned to the client.
    return {}


def handle_chart_data(chart_name):

    """Passed the filename of a particular chart"""

    # This function would return chart data computed from
    # whatever sources are used.
    # It returns an object that will be JSON encoded and
    # returned to the client.
    return {}


###############################################################
#
# Handles requests for files that return JSON objects.
#
###############################################################


def dynamic_handler(file_path):

    file_data = ''

    # Possible requests are:
    #   /charts/templates                       : list of template files
    #   /charts/templates/<templatename.json>   : particular template file
    #   /charts/charts                          : list of chart files
    #   /charts/charts/<chartname.json>         : particular chart file
    #   /charts/data/<chartname.json>           : particular chart data

    # Break the file path into parts.
    parts = file_path.split('/')
    # Return if wrong number of parts.
    if len(parts) < 2 or len(parts) > 3:
        return file_data
    # Return if wrong first part.
    if not parts[0] == 'charts':
        return file_data
    # Return if illegal second part.
    if not parts[1] == 'charts' and not parts[1] == 'templates' and not parts[1] == 'data':
        return file_data
    #
    # Two elements is a request for a list of files.
    #
    if len(parts) == 2:
        # If asking for a list of template files.
        if parts[1] == 'templates':
            templates = fnmatch.filter(os.listdir(chart_path + 'templates') , '*.json')
            file_data = json.JSONEncoder().encode(templates)
        # Else if asking for a list of chart files.
        elif parts[1] == 'charts':
            templates = fnmatch.filter(os.listdir(chart_path) , '*.json')
            file_data = json.JSONEncoder().encode(templates)
    #
    # Three elements is a request for either a particular template or chart
    # file, or chart data.
    #
    else:
        # If asking for template file.
        if parts[1] == 'templates':
            templates = fnmatch.filter(os.listdir(chart_path + 'templates') , '*.json')
            if parts[2] in templates:
                fd = open(chart_path + 'templates/' + parts[2] , 'r')
                file_data = fd.read()
                fd.close()
        # Else if asking for chart file.
        elif parts[1] == 'charts':
            templates = fnmatch.filter(os.listdir(chart_path) , '*.json')
            if parts[2] in templates:
                fd = open(chart_path + parts[2] , 'r')
                file_data = fd.read()
                fd.close()
        # Else if asking for chart data.
        elif parts[1] == 'data':
            # Delegate to custom function
            file_data = handle_chart_data(parts[2])
        # Else unknown request.
        else:
            pass

    return file_data


###############################################################
#
# General purpose server request handler.
#
# If the GET url begins with '/charts', we circumvent the normal
# return process and call 'dynamic_handler()'. This function
# will generate a JSON object that will return:
#   1. chart templates in the /charts/templates folder
#   2. chart configurations used when creating a chart
#   3. chart data files that are used to update chart data
#
###############################################################


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        result_code = 200
        content_type = 'text/html'

        # Get the requested file with path.
        file_path = self.path
        # If we're looking for dynamic files.
        if file_path.startswith('/charts'):
            # Remove leading and trailing '/' characters.
            file_path = file_path[1:]
            if file_path.endswith('/'):
                file_path = file_path[:-1]
            # Handle this request elsewhere.
            file_data = dynamic_handler(file_path)
            # If error.
            if len(file_data) == 0:
                result_code = 404
        # Else looking for a particular file name.
        else:
            # If the path is '/' or 0-length.
            if file_path == '/' or len(file_path) == 0:
                # Going with index.
                file_path = 'index.html'
            # Get the file name.
            file_name = os.path.basename(file_path)
            # Get the file extension (minus the '.').
            ext = pathlib.Path(file_name).suffix[1:]
            # One of our known types?
            if ext in mime_types:
                # Create relative path.
                rel_name = client_path + file_name
                # If the file exists.
                if os.path.isfile(rel_name):
                    # Open the file.
                    fd = open(rel_name , 'r')
                    # Read it.
                    file_data = fd.read()
                    # Close it.
                    fd.close()
                    # If css was requested we must modify the content for IE.
                    if ext == 'css':
                        content_type = 'text/css'
                # Else file does not exist.
                else:
                    result_code = 404
            # Else we don't handle it.
            else:
                result_code = 404
        # If file not present.
        if result_code == 404:
            file_data = 'File not found'
        # Send the headers.
        self.send_response(result_code)
        self.send_header('Content-type' , content_type)
        self.end_headers()
        # Send the response.
        self.wfile.write(bytes(file_data , 'UTF-8'))
        return

    def do_POST(self):
        #
        # POST included for completeness, but not used in basic example.
        #

        # Originally 'content-length', but Postman uses 'Content-Length'???
        try:
            content_str = self.headers['content-length']
        except KeyError:
            try:
                content_str = self.headers['Content-Length']
            except KeyError:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(bytes('Unknown content length'))
                return
        content_len = int(content_str)
        # Data returned as byte[].
        post_bytes = self.rfile.read(content_len)
        # Convert to string.
        post_string = post_bytes.decode("utf-8")
        try:
            # Convert string to json.
            post_json = json.JSONDecoder().decode(post_string)
            # Get result object from specialized POST handler.
            result_obj = handle_post_request(post_json)
            # Encode the returned object as a string.
            result_string = json.JSONEncoder().encode(result_obj)
        except json.JSONDecodeError:
            result_string = '{"error": "JSON decode error"}'
        # Send the headers.
        self.send_response(200)
        self.end_headers()
        # Send the result.
        self.wfile.write(bytes(result_string , 'UTF-8'))
        return


###############################################################
#
# Main; just starts the http server.
#
###############################################################


if __name__ == '__main__':

    # If we were not started from the top level.
    if not os.path.isdir('client'):
        # Need to redefine folder paths.
        client_path = '../client/'
        chart_path = '../charts/'
    server = HTTPServer(('localhost', 8080) , RequestHandler)
    print('Starting server at http://localhost:8080')
    server.serve_forever()
