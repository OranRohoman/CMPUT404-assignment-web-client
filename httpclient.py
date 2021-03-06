#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

#Citations:
#referenced this document for each time i used the urllib.parse.
#https://docs.python.org/3/library/urllib.parse.html

#referenced code by Adam Smith
#to encode post arguments.
#https://stackoverflow.com/questions/40557606/how-to-url-encode-in-python-3

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        body = data.split("\r\n")
        code = body[0].split(" ")
        #print("code\n",code[1])
        return int(code[1])

    def get_headers(self,data):
        body = data.split("\r\n\r\n")
        #print("headers\n",body[0])
        return body[0]

    def get_body(self, data):
        body = data.split("\r\n\r\n")
        #print("body\n",body[1])
        return body[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()


    def parse(self,url):
        pass
    
    def get_port(self):
        if(self.parsed.port ==None):
            if(self.scheme == "https"):
                return 443
            elif(self.scheme == "http"):
                return 80
        return self.parsed.port
    def get_path(self,path):
        if(path == ""):
            return "/"
        return path

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    
    def GET(self, url, args=None):
        self.parsed = urllib.parse.urlparse(url)
        self.scheme = self.parsed.scheme
        self.port = self.get_port()
        self.host = self.parsed.hostname
        
        self.connect(self.host,self.port)
        self.path = self.get_path(self.parsed.path)

        # print("scheme: ",self.scheme)
        # print("port: ",self.port)
        # print("host: ",self.host)
        # print("path: ",self.path)
        # print()

        self.request = "GET "+self.path+" HTTP/1.1\r\n" + "Host: "+self.host+"\r\n" + \
            "Connection: close\r\n\r\n"

        self.sendall(self.request)
        self.data = self.recvall(self.socket)
        
        #print(self.request)
        #return "we testing"
        print(self.data)
        code = self.get_code(self.data)
        body = self.get_body(self.data)
        self.get_headers(self.data)
        self.close()
        return HTTPResponse(code, body)


    def POST(self, url, args=None):
        self.parsed = urllib.parse.urlparse(url)
        self.scheme = self.parsed.scheme
        self.port = self.get_port()
        self.host = self.parsed.hostname
        
        self.connect(self.host,self.port)
        self.path = self.get_path(self.parsed.path)

        
        self.content = ""
        if(args != None):
            self.content = urllib.parse.urlencode(args)

        
        
        self.request = "POST "+self.path+" HTTP/1.1\r\n" + "Host: "+self.host+"\r\n" + \
                "Connection: close\r\n"+"Content-Type: application/x-www-form-urlencoded\r\n"+ \
                    "Content-Length: "+str(len(self.content))+"\r\n\r\n"+ \
                        self.content
            
        #print(self.request)
        self.sendall(self.request)
        self.data = self.recvall(self.socket)
        
        #return "we testing"
        print(self.data)
        code = self.get_code(self.data)
        body = self.get_body(self.data)
        self.get_headers(self.data)
        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
