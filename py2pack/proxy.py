# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Sascha Peilicke <sascha@peilicke.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import http.client as httplib
except ImportError:
    import httplib
try:
    import xmlrpc.client as xmlrpclib
except ImportError:
    import xmlrpclib


class ProxiedTransport(xmlrpclib.Transport):
    def set_proxy(self, proxy):
        self.proxy = proxy

    def make_connection(self, host):
        self.realhost = host
        return httplib.HTTP(self.proxy)

    def send_request(self, connection, handler, request_body):
        connection.putrequest('POST', 'http://{0}{1}'.format(self.realhost, handler))

    def send_host(self, connection, host):
        connection.putheader('Host', self.realhost)
