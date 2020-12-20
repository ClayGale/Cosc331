import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from urllib.request import urlopen

hostName = "localhost"
serverPort = 8080

resourceService = "http://138.197.148.107/"

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.getPage() == "/paragraph":
            input = self.getParams() # receiving length parameter
            try:
                length = int(input["x"])
            except:
                self.set_headers(400)
                self.wfile.write(bytes("invalid input", "utf-8"))
            output = "" # base string to be appended too
            url = resourceService + "sentence"

            while len(output.split()) < length: # running the loop as long as the paragraph is below desired length
                try:
                    resource = urlopen(url)
                except:
                    self.set_headers(503)
                    self.wfile.write(bytes("resource server unavailable", "utf-8"))
                resource = resource.read()
                resource = resource.decode("utf-8")
                print(resource)

                output += " " + resource # appending the paragraph together

            print(output)

            self.set_headers(200)
            self.wfile.write(bytes(output, "utf-8"))

        if self.getPage() == "/random":
            input = self.getParams() # receiving range parameters
            try:
                lowerBound = int(input["x"])
                upperBound = int(input["y"])
            except:
                self.set_headers(400)
                self.wfile.write(bytes("invalid input", "utf-8"))
            range = upperBound - lowerBound # calculating range and sending request
            url = resourceService + "randint/" + str(range)

            try:
                resource = urlopen(url)
            except:
                self.set_headers(503)
                self.wfile.write(bytes("resource server unavailable", "utf-8"))
            resource = resource.read()
            resource = resource.decode("utf-8")
            print(resource)

            resource = int(resource)
            output = str(resource + lowerBound) # calculating final result

            print(output)

            self.set_headers(200)
            self.wfile.write(bytes(output, "utf-8"))


        #if self.getPage() == "/random":

    def getPage(self): #skeleton code
        return parse.urlsplit(self.path).path

    def getParams(self): #skeleton code
        output = {}
        queryList = parse.parse_qs(parse.urlsplit(self.path).query)
        for key in queryList:
            if len(queryList[key]) == 1:
                output[key] = queryList[key][0]
        return output

    def set_headers(self, responseCode): #skeleton code
        self.send_response(responseCode)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-Headers', "*")
        self.end_headers()

if __name__ == "__main__": #skeleton code
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