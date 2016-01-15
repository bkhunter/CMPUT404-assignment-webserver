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
        while self.data[i] != '\n':
            message += self.data[i]
            i+=1
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
        response = initLine + '\n' + dateLine + '\n' + lenLine + '\n' + mimeLine + '\n' + '\r\n\r\n' + content
        return response

    def notFound(self):
        HTTP_Code = "HTTP/1.1 404 NOT FOUND"
        date = "Date:"+ str(datetime.datetime.now())
        errorMsg = "<html><head><title> NOT FOUND :( .</title></head><body><p>Error 404 File Not Found.</p></body></html>" 
        errorLength = "Content-Length:" + str(len(errorMsg))
        mimeType = 'text/html; charset=utf-8'

        response = self.makeResponse(HTTP_Code,date,errorLength,mimeType,errorMsg)
        print response
        return response
        
    def do_GET(self,path):
        cwd = os.getcwd()
        curDir = cwd + '/www'
        date = "Date:"+ str(datetime.datetime.now())
        isFile = False;

        if isValidPath(path) :
            if path.endswith('.css'):
                mimeType = 'text/css; charset=utf-8'
                isFile = True
            elif path.endswith('.html'):
                mimeType = 'text/html; charset=utf-8'
                isFile = True
            try:
                if isFile:
                    if path == '/deep.css':
                        toOpen = curDir + '/deep' + path
                        display = open(toOpen)
                        HTTP_Code = "HTTP/1.1 200 OK"
                        data = display.read()
                        length = str(len(data))
                        display.close()
                        response = self.makeResponse(HTTP_Code,date,length,mimeType,data)
                        return response
                    else:
                        x = self.notFound()
                        return x
                else:
                    x = self.notFound()
                    return x
            except IOError:
                 x = self.notFound()
                 return x
                
                    # elif path.endswith('/'): # if the path ends with / display index.html
                    #     display = open(toOpen+'index.html')
                    #     self.send_response(200)
                    #     self.send_header('Content-type', 'text/html')
                    #     self.end_headers()
                    #     self.wfile.write(display.read())
                    #     display.close()
                    # elif path.endswith('deep'): # corner case
                    #     display = open(toOpen+'/index.html')
                    #     self.send_response(200)
                    #     self.send_header('Content-type', 'text/html')
                    #     self.end_headers()
                    #     self.wfile.write(display.read())
                    #     display.close()
        
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        print "---------"
        message,path = self.parseRequest()
        if message[:3] == 'GET':
            print message
            print path
            response = self.do_GET(path)
        else:
            response = self.notFound()
            
        good_response = "HTTP/1.0 200 OK\nContent-Type:text/html"
        self.request.sendall(response)
        
        #print "{} wrote:".format(self.client_address[0])
        #http_response = "Hello World"
        #self.request.sendall(http_response)
        #self.send_response(200)

    

class MyWebServer2(BaseHTTPRequestHandler):

    def do_GET(self):
        cwd = os.getcwd()
        curDir = cwd + '/www'
        mimetype = ''
        isFile = False;
        path = self.path

        if isValidPath(path) :
            if path.endswith('.css'):
                mimetype = 'text/css'
                isFile = True
            elif path.endswith('.html'):
                mimetype = 'text/html'
                isFile = True
                toOpen = curDir+path
            try:
                if isFile:
                    if path == '/deep.css':
                        toOpen = curDir + '/deep' + path
                        display = open(toOpen)
                        self.send_response(200)
                        self.send_header('Content-type', mimetype)
                        self.end_headers()
                        self.wfile.write(display.read())
                        display.close()
                    elif path.endswith('/'): # if the path ends with / display index.html
                        display = open(toOpen+'index.html')
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(display.read())
                        display.close()
                    elif path.endswith('deep'): # corner case
                        display = open(toOpen+'/index.html')
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(display.read())
                        display.close()
            except IOError:
                self.send_error(404)
        else:
            self.send_error(404)
            # self.send_response(404)
            # self.send_header("Content-type", "text/html")
            # self.end_headers()
            # self.wfile.write("<html><head><title> 404 :( .</title></head>")
            # self.wfile.write("<body><p>Error 404 File Not Found.</p>")
            # self.wfile.write("</body></html>")
                            
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

