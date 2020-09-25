# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 13:55:35 2020
@author: generic
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import time, sys, base64
from urllib import parse

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if self.getPage() == '/':
            self.wfile.write(bytes("Hello World!", "utf-8"))

    # Gets the query parameters of a request and returns them as a dictionary
    def getParams(self):
        output = {}
        queryList = parse.parse_qs(parse.urlsplit(self.path).query)
        for key in queryList:
            if len(queryList[key]) == 1:
                output[key] = queryList[key][0]
        return output

    # Returns a string containing the page (path) that the request was for
    def getPage(self):
        return parse.urlsplit(self.path).path

    def encode(self, key, plaintext):
        output = []
        for i in range(len(plaintext)):
            key_c = key[i % len(key)]
            enc_c = (ord(plaintext[i]) + ord(key_c)) % 256
            output.append(enc_c)
        return base64.urlsafe_b64encode(bytes(output))

    def decode(self, key, ciphertext):
        output = []
        ciphertext = base64.urlsafe_b64decode(ciphertext)
        for i in range(len(ciphertext)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ciphertext[i] - ord(key_c)) % 256)
            output.append(dec_c)
        return "".join(output)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started at 127.0.0.1:8080")

    try:
        webServer.serve_forever()
    except:
        webServer.server_close()
        print("Server stopped.")
        sys.exit()

    webServer.server_close()
    print("Server stopped.")
    sys.exit()