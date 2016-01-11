#  coding: utf-8 
import SocketServer
import sys
import urllib2
import os

#so I can handle get requests
from BaseHTTPServer import BaseHTTPRequestHandler

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

## BEN KEEP LOOKING INTO HOW TO SERVE A LOCAL DIRECTORY


# class MyWebServer(SocketServer.BaseRequestHandler):

#     def do_GET(self):
#         if self.path == '/www':
#             print "did it work?"
#         self.send_response(200)
    
#     def handle(self):
#         self.data = self.request.recv(1024).strip()
#         print ("Got a request of: %s\n" % self.data)
#         #print "{} wrote:".format(self.client_address[0])
#         http_response = "Hello World"
#         self.request.sendall(http_response)
#         #self.send_response(200)

def checkDir(path):
    return '..' in path
       

class MyWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        cwd = os.getcwd()
        curdir = cwd + '/www'
        path = self.path
        toOpen = curdir+path
        try:
            if toOpen.endswith(".css"):
                if checkDir(toOpen):
                    raise IOError("path traversal attack!")
                else:
                    display = open(toOpen)
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    self.wfile.write(display.read())
                    display.close()
            elif path.endswith('/') and (toOpen[-1] != toOpen[-2]): # explicitly serve index.html
                if checkDir(toOpen):
                    raise IOError("path traversal attack!")
                else:
                    display = open(toOpen+'index.html')
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(display.read())
                    display.close()
            else:
                if checkDir(toOpen):
                    print "AAAAAAAAAAH"
                    raise IOError("path traversal attack!")
                else:
                    display = open(toOpen)
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(display.read())
                    display.close()
        except IOError:
            #e = sys.exc_info()[0]
            #print e
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("<html><head><title> 404 :( .</title></head>")
            self.wfile.write("<body><p>Error 404 File Not Found.</p>")
            self.wfile.write("</body></html>")
            
if __name__ == "__main__":
    HOST = "localhost" 
    PORT =  8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print 'Serving HTTP on port %s ...' % PORT
    server.serve_forever()

