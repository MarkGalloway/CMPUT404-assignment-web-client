#!/usr/bin/env python
# coding: utf-8
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
#
# run python ourtests.py

import unittest
import httpclient


class TestHTTPClient(unittest.TestCase):

    def testConnect(self):
        http = httpclient.HTTPClient()
        http.connect("www.google.ca", 80)
        http.disconnect()

    def testget_hostname(self):
        http = httpclient.HTTPClient()
        http.get_hostname("www.google.ca")

    def test_full_url(self):
        http = httpclient.HTTPClient()
        host, port, path, query = http.decomposeUrl("http://www.google.ca:80/some/path/index.html")
        self.assertTrue(host == "www.google.ca")
        self.assertTrue(port == 80)
        self.assertTrue(path == "/some/path/index.html")

    def test_no_port(self):
        http = httpclient.HTTPClient()
        host, port, path, query = http.decomposeUrl("http://www.google.ca/some/path/index.html")
        self.assertTrue(host == "www.google.ca")
        self.assertTrue(port == 80)
        self.assertTrue(path == "/some/path/index.html")

    def test_no_path(self):
        http = httpclient.HTTPClient()
        host, port, path, query = http.decomposeUrl("http://www.google.ca:75")
        self.assertTrue(host == "www.google.ca")
        self.assertTrue(port == 75)
        self.assertTrue(path == "/")

    def test_no_path_no_port(self):
        http = httpclient.HTTPClient()
        host, port, path, query = http.decomposeUrl("www.google.ca")
        self.assertTrue(host == "www.google.ca")
        self.assertTrue(port == 80)
        self.assertTrue(path == "/")

    def test_get_code(self):
        http = httpclient.HTTPClient()
        response = "HTTP/1.1 302 Found"
        code = http.get_code(response)
        self.assertTrue(code == 302)

    # To test:
    # Test  get_body
    # Test  get_header
    # URL with username/password??
    # URL with fancy encodings to make sure we handle them correctly
    # URL with / / /  path gets transcoded to \ \ \ ??? Does this make sense??
    # Query strings


if __name__ == '__main__':
    unittest.main()