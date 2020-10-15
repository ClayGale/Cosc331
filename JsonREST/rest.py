# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 12:52:31 2020

@author: generic
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 01:03:56 2020

@author: KoBoLd
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import time, json
from urllib import parse
from json import JSONDecodeError

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    
    myDict = {}
    
    # You can pass an integer statusCode (i.e. 200, 404, etc) to this function to return a specific HTTP status
    def set_headers(self, statusCode):
        self.send_response(statusCode)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-Headers', "*")
        self.send_header('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, PATCH, OPTIONS")
        self.end_headers()
    
    def do_GET(self):
        print("GET REQUEST")
        # TO-DO: FETCH JSON OBJECT OR SPECIFIC VALUE
        
    def do_POST(self):
        print("POST REQUEST")
        # TO-DO: CREATE JSON OBJECT
        
    def do_PUT(self):
        print("PUT REQUEST")
        # TO-DO: OVERWRITE EXISTING JSON OBJECT
        
    def do_DELETE(self):
        print("DELETE REQUEST")
        # TO-DO: DELETE EXISTING JSON OBJECT
        
    def do_PATCH(self):
        print("PATCH REQUEST")
        # TO-DO: SELECTIVELY OVERWRITE KEY-VALUE PAIRS OF A JSON OBJECT
        
    # This is necessary, as OPTIONS is used to check if the service supports HTTP 1.1 verbs (PUT, PATCH, DELETE)    
    def do_OPTIONS(self):
        self.set_headers(200)
        
    # This function retrieves the current URI that has been requested by the client   
    def getURI(self):
        return parse.urlsplit(self.path).path
    
    # This function gets any query string parameters that were part of the request
    def getParams(self):
        output = {}
        queryList = parse.parse_qs(parse.urlsplit(self.path).query)
        for key in queryList:
            if len(queryList[key]) == 1:
                output[key] = queryList[key][0]
        return output
    
    # This function retrieves the request body data
    def getBody(self):
        return self.rfile.read(int(self.headers.get('Content-Length')))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    webServer.serve_forever()