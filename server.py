#  coding: utf-8 
import SocketServer
import sys
import os

# See README for detailed source and licensing information pertaining to
# Ben Hunter, Abram Hindle, Eddie Antonio Santos

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


# checks the parsed path, and ensures it is valid
def isValidPath(path):
    path = os.path.abspath(path)     # this evaluates any .. or ./ in the path
    
    # List of all the paths that I want to serve
    return path in ['/', '/index.html', '/base.css','/deep.css','/deep','/deep/', '/deep/index.html', '/deep/deep.css']


class MyWebServer(SocketServer.BaseRequestHandler):

    #iterate through the request and determine the verb and path
    def parseRequest(self):
        message = ''
        path = ''
        isInPath = False
        i = 0

        #get the verb
        for element in self.data:
            if element != '\n':
                message += element
            else:
                break

        #get the path
        for char in message:
            if char == '/':
                isInPath = True
            if isInPath:
                if char == ' ':
                    break
                else:
                    path += char
                            
        return message,path
        
    # Helper function that takes each line of the HTTP response
    # and puts it all together with correct line endings
    def makeResponse(self,initLine, lenLine, mimeLine, content):
        response = initLine + '\r\n'+ lenLine + '\r\n' + mimeLine + '\r\n\r\n' + content
        return response


    # When a HTTP 404 encountered call this function, which creates 
    # the appropriate response
    def notFound(self):
        HTTP_Code = "HTTP/1.1 404 NOT FOUND"
        errorMsg = "<html><head><title> 404 NOT FOUND </title></head><body><p>Error 404 File Not Found.</p></body></html>" 
        errorLength = "Content-Length:" + str(len(errorMsg))
        mimeType = 'Content-Type: text/html; charset=utf-8'

        response = self.makeResponse(HTTP_Code,errorLength,mimeType,errorMsg)
        return response
        
    #Handle GET Requests
    def do_GET(self,path):
        cwd = os.getcwd()
        curDir = cwd + '/www'
        toOpen = None

        if isValidPath(path):
            if path.endswith('.css'):
                mimeType = 'Content-Type:text/css; charset=utf-8'
            elif path.endswith('.html') :
                mimeType = 'Content-Type:text/html; charset=utf-8'
                toOpen = curDir + path
            elif path.endswith('/'): # display index.html
                mimeType = 'Content-Type:text/html; charset=utf-8'
                toOpen = curDir + path + 'index.html'
            elif path.endswith('deep'): # display deep.html
                mimeType = 'Content-Type:text/html; charset=utf-8'
                toOpen = curDir + path + '/index.html'

            try:
                if path == '/deep.css':
                    # redirect!
                    HTTP_Code = "HTTP/1.1 301 Moved Permanently"
                    location = "Location: http://127.0.0.1:8080/deep/deep.css"
                    response = HTTP_Code + '\r\n' + location + '\r\n\r\n'
                    return response
                else:  
                    if toOpen is None:
                        toOpen = curDir + path
                    contents = open(toOpen,"r")
                    HTTP_Code = "HTTP/1.1 200 OK"
                    data = contents.read()
                    length = "Content-Length:"+ str(len(data))
                    contents.close()
                    response = self.makeResponse(HTTP_Code,length,mimeType,data)
                    return response
            except IOError:
                return self.notFound()
        else:
            return self.notFound()
                
    # Method to handle all requests
    def handle(self):
        self.data = self.request.recv(1024).strip()
        message,path = self.parseRequest()

        #Currently only handles GET requests
        if message[:3] == 'GET':
            response = self.do_GET(path)
        else:
            response = self.notFound()


        self.request.sendall(response)

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
