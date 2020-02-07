#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, Cole Boytinck, https://github.com/tywtyw2002, and https://github.com/treedust
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
# you may use urllib to encode data appropriately
import urllib.parse

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
        self.socket.settimeout(2)
        return None

    def get_code(self, data):
        return int(data[0].split(" ")[1])

    def get_headers(self,data):
        return data.split("\r\n")

    def get_body(self, data):
        return ""

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        return self.recvall()

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self):
        buffer = bytearray()
        done = False
        try:
            while not done:
                part = self.socket.recv(1024)
                if (part):
                    buffer.extend(part)
                else:
                    done = not part
        except socket.timeout:
            print("Timeout Detected")
        return buffer.decode('utf-8')
        
    def getHost(self,  url):
        data = urllib.parse.urlparse(url)
        return data.hostname
    
    def getPort(self,  url):
        data = urllib.parse.urlparse(url)
        if data.port == None:
            return 80
        return data.port
    
    def getPath(self,  url):
        data = urllib.parse.urlparse(url)
        if data.path == "":
            return "/"
        return data.path

    def GET(self, url, args=None):
        request = """GET {path} HTTP/1.1\r
Host: {host}\r\n\r\n""".format(path=self.getPath(url),  host=self.getHost(url))
        self.connect(self.getHost(url), self.getPort(url))
        data = self.sendall(request)
        print(data)
        headers = self.get_headers(data)
        code = self.get_code(headers)
        self.close()
        return HTTPResponse(code, data)
        
    def args_to_request(self,  args):
        if args == None:
            return ""
        else:
            return urllib.parse.urlencode(args)

    def POST(self, url, args=None):
        request_data = self.args_to_request(args)
        request = """POST {path} HTTP/1.1\r
Host: {host}\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: {length}\r
\r
{data}""".format(path=self.getPath(url),  data=request_data,  length=(len(request_data)),  host=self.getHost(url))
        self.connect(self.getHost(url), self.getPort(url))
        data = self.sendall(request)
        headers = self.get_headers(data)
        body = headers[-1]
        code = self.get_code(headers)
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
