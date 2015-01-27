#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# Copyright 2015 Mark Galloway
# Copyright 2015 Tamara Bain
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
import urllib


def help():
    print "httpclient.py [GET/POST] [URL]\n"


class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    # def get_host_port(self,url):

    # Look up host by name
    def get_hostname(self, host):
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            print 'Hostname could not be resolved. Exiting'
            sys.exit()

    # Connect to host/port via sockets
    def connect(self, host, port):
        self.sock = None
        try:
            # Create an AF_INET, STREAM socket (TCP)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' \
                  + str(msg[0]) + ' , Error message : ' + msg[1]
            sys.exit()

        remote_ip = self.get_hostname(host)
        # Establish connection
        self.sock.connect((remote_ip, port))

    # Disconnect socket
    def disconnect(self):
        self.sock.close()

    def get_code(self, data):
        return int(data.split()[1])

    def get_headers(self, data):
        start = data.find("\r\n")
        end = data.find("\r\n\r\n")
        if start == -1:
            return ''
        else:
            return data[start + 2:end]

    def get_body(self, data):
        start = data.find("\r\n\r\n")
        if start == -1:
            return ''
        else:
            return data[start + 4:]

    def send_and_receive(self, host, port, request):
        # Connect To Host
        self.connect(host, port)

        # Send Request
        try:
            self.sock.sendall(request.encode("UTF8"))
        except socket.error:
            # Send failed
            print 'Send failed'
            sys.exit()

        # Receive Data
        data = self.recvall(self.sock)

        # DEBUG
        # print(data)

        # Disconnect From Host
        self.disconnect()

        return data

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
        return str(buffer)

    # Break down a URL into its host,port,path components
    def decomposeUrl(self, url):
        regex = "(?:http://)?(?P<host>[^:/]+).?(?P<port>[0-9]*)(?P<path>[^?]*).?(?P<query>.*)?"
        match = re.search(regex, url)
        host = match.group('host')
        port = match.group('port')
        if port == '':
            port = 80
        else:
            port = int(port)
        path = match.group('path')
        if path == '' or path[0] != '/':
            path = '/' + path
        query = match.group('query')
        return host, port, path, query

    # Perform a HTTP GET request to the URL argument
    def GET(self, url, args=None):
        # Build GET Request
        host, port, path, query = self.decomposeUrl(url)
        encoded_path = urllib.quote(path)
        encoded_host = urllib.quote(host)
        if query != '':
            encoded_path + '?' + urllib.quote(query)

        request = "GET " + encoded_path + " HTTP/1.1\r\n" \
            + "User-Agent: cmput410client\r\n" \
            + "Host: " + encoded_host + "\r\n" \
            + "Accept: */*\r\n\r\n"

        # Send the request and get the response
        data = self.send_and_receive(host, port, request)

        # DEBUG
        # print(data)

        # Parse Data
        code = self.get_code(data)
        body = self.get_body(data)

        return HTTPRequest(code, body)

    # TODO: encode query arguments using urllib
    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, args)
        else:
            return self.GET(url, args)

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command(sys.argv[2], sys.argv[1])
    else:
        print client.command(sys.argv[1], command)
