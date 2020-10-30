from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import base64
from urllib import request, parse

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    
    # Set the HTTP status code and response headers
    def set_headers(self, responseCode):
        self.send_response(responseCode)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-Headers', "*")
        self.end_headers()
    
        
    def do_POST(self):
        requestData = self.getRequestData()

        myPrivateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend = default_backend()
        )

        myPublicKey = myPrivateKey.public_key()

        myPEM = myPublicKey.public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        )

        publicKeyEndpoint = requestData.get('publickey')
        remotePEM = request.urlopen(publicKeyEndpoint)
        remotePublicKey = serialization.load_pem_public_key(remotePEM)

        plaintext = requestData.get('plaintext')
        ciphertext = remotePublicKey.encrypt(bytes(plaintext, 'utf-8'), padding.PKCS1v15)
        ciphertext = base64.b64encode(ciphertext)

        encryptionEndpoint = requestData.get('endpoint')
        postParameters = parse.urlencode({"ciphertext" : ciphertext, "publickey" : myPEM}).encode()
        encryptRequest = request.Request(encryptionEndpoint, data = postParameters)
        tokenResponse = request.urlopen(encryptRequest).read()
        tokenResponse = base64.b64decode(tokenResponse)

        decryptedToken = myPrivateKey.decrypt(tokenResponse, padding.PKCS1v15)
        decryptedToken = decryptedToken.decode('utf-8')

        fetchURI = requestData.get('fetch')
        fetchURI += decryptedToken

        self.set_headers(200)
        self.wfile.write(bytes("Message Juggled: " + fetchURI, 'utf-8'))

    def getRequestData(self):
        body = self.rfile.read(int(self.headers.get('Content-Length')))
        body = body.decode("utf-8")
        return dict(parse.parse_qsl(body))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except:
        webServer.server_close()
        print("Server stopped.")
        sys.exit()
    webServer.server_close()
    print("Server stopped.")
    sys.exit()