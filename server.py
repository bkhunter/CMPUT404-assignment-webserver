#  coding: utf-8 
import SocketServer
import sys
import urllib2
import os
import datetime

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

        # an initial line 
        # zero or more header lines
        # blank line 
        # message body'''

        # '''
        # HTTP/1.1 CODE MSG
        # Content-Type: text/mimetype
        # Content-Length: length
        # msg

        #KNOWN to work:
        #HTTP/1.1 404 NOT FOUND
        #Date:2016-01-14 00:16:21.472463
        #Content-Length:101
        #text/html; charset=utf-8


        #<html><head><title> NOT FOUND :( .</title></head><body><p>Error 404 File Not Found.</p></body></html>


def isValidPath(path):
    return path in ['/', '/index.html', '/base.css','/deep.css', '/deep', '/deep/', '/deep/index.html', '/deep/deep.css']


class MyWebServer1(SocketServer.BaseRequestHandler):

    def parseRequest(self):
        message = ''
        path = ''
        isInPath = False
        i = 0
        for element in self.data:
            if element != '\n':
                message += element
            else:
                break
        for char in message:
            if char == '/':
                isInPath = True
            if isInPath:
                if char == ' ':
                    break
                else:
                    path += char
                            
        return message,path
        
    def makeResponse(self,initLine, dateLine, lenLine, mimeLine, content):
        response = initLine + '\r\n' + dateLine + '\r\n'+ lenLine + '\r\n' + mimeLine + '\r\n\r\n' + content
        return response

        # HTTP/1.1 200 OK
        # Date:2016-01-15 14:43:15.668762
        # 470
        # text/html; charset=utf-8

        # HTTP/1.1 200 OK
        # Date:2016-01-15 14:43:15.761839
        # 48
        # text/css; charset=utf-8

        # HTTP/1.1 404 NOT FOUND
        # Date:2016-01-15 14:45:38.355325
        # Content-Length:101
        # text/html; charset=utf-8


    def notFound(self):
        HTTP_Code = "HTTP/1.1 404 NOT FOUND"
        date = "Date:"+ str(datetime.datetime.now())
        errorMsg = "<html><head><title> NOT FOUND :( .</title></head><body><p>Error 404 File Not Found.</p></body></html>" 
        errorLength = "Content-Length:" + str(len(errorMsg))
        mimeType = 'Content-Type: text/html; charset=utf-8'

        response = self.makeResponse(HTTP_Code,date,errorLength,mimeType,errorMsg)
        return response
        
    def do_GET(self,path):
        cwd = os.getcwd()
        curDir = cwd + '/www'
        date = "Date:"+ str(datetime.datetime.now())
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
                    toOpen = curDir + '/deep' + path
                    contents = open(toOpen,"r")
                    HTTP_Code = "HTTP/1.1 200 OK"
                    data = contents.read()
                    length = "Content-Length:"+ str(len(data))
                    contents.close()
                    response = self.makeResponse(HTTP_Code,date,length,mimeType,data)
                    return response
                else:  
                    if toOpen is None:
                        toOpen = curDir + path
                    contents = open(toOpen,"r")
                    HTTP_Code = "HTTP/1.1 200 OK"
                    data = contents.read()
                    length = "Content-Length:"+ str(len(data))
                    contents.close()
                    response = self.makeResponse(HTTP_Code,date,length,mimeType,data)
                    return response
            except IOError:
                x = self.notFound()
                return x
        else:
            x = self.notFound()
            return x
                
    def handle(self):
        self.data = self.request.recv(1024).strip()
        message,path = self.parseRequest()
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
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer1)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print 'Serving HTTP on port %s ...' % PORT
    server.serve_forever()
