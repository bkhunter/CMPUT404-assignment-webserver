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
        response = initLine + '\r\n' + lenLine + '\r\n' + mimeLine + '\r\n\r\n' + content
        #+ dateLine + '\n'      
        return response

    def notFound(self):
        HTTP_Code = "HTTP/1.1 404 NOT FOUND"
        date = "Date:"+ str(datetime.datetime.now())
        errorMsg = "<html><head><title> NOT FOUND :( .</title></head><body><p>Error 404 File Not Found.</p></body></html>" 
        errorLength = "Content-Length:" + str(len(errorMsg))
        mimeType = 'text/html; charset=utf-8'

        response = self.makeResponse(HTTP_Code,date,errorLength,mimeType,errorMsg)
        return response
        
    def do_GET(self,path):
        cwd = os.getcwd()
        curDir = cwd + '/www'
        date = "Date:"+ str(datetime.datetime.now())
        toOpen = None

        if isValidPath(path):
            if path.endswith('.css'):
                print('css')
                mimeType = 'text/css; charset=utf-8'
            elif path.endswith('.html') :
                mimeType = 'text/html; charset=utf-8'
                toOpen = curDir + path
            elif path.endswith('/'): # display index.html
                mimeType = 'text/html; charset=utf-8'
                toOpen = curDir + path + 'index.html'
            elif path.endswith('deep'): # display deep.html
                mimeType = 'text/html; charset=utf-8'
                toOpen = curDir + path + '/index.html'

            try:
                print 'In try'
                if path == '/deep.css':
                    toOpen = curDir + '/deep' + path
                    contents = open(toOpen,"r")
                    HTTP_Code = "HTTP/1.1 200 OK"
                    data = contents.read()
                    length = str(len(data))
                    contents.close()
                    response = self.makeResponse(HTTP_Code,date,length,mimeType,data)
                    return response
                else:
                    
                    if toOpen is None:
                        toOpen = curDir + path
                    print toOpen
                    contents = open(toOpen,"r")
                    HTTP_Code = "HTTP/1.1 200 OK"
                    data = contents.read()
                    length = str(len(data))
                    contents.close()
                    response = self.makeResponse(HTTP_Code,date,length,mimeType,data)
                    return response
            except:
                x = self.notFound()
                return x
        else:
            x = self.notFound()
            return x
                
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        message,path = self.parseRequest()
        print path
        if message[:3] == 'GET':
            print message
            print path
            response = self.do_GET(path)
        else:
            response = self.notFound()

        print response
        self.request.sendall(response)
        
        #print "{} wrote:".format(self.client_address[0])
        #http_response = "Hello World"
        #self.request.sendall(http_response)
        #self.send_response(200)

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


      # elif path.endswith('/'): # if the path ends with / display index.html
      #               print('////!!!!////')
      #               contents = open(toOpen+'index.html')
      #               HTTP_Code = "HTTP/1.1 200 OK"
      #               mimeType = 'text/html; charset=utf-8'
      #               data = contents.read()
      #               length = str(len(data))
      #               contents.close()
      #               response = self.makeResponse(HTTP_Code,date,length,mimeType,data)
      #               return response
      #           else:
      #               x = self.notFound()
      #               return x



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
