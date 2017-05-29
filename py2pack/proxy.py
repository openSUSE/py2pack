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
import sys
import six.moves.http_client as httplib
from six.moves.urllib.parse import urlparse
from six.moves import xmlrpc_client as xmlrpclib

# workaround python httplib bug (#7776)
try:
    import gzip
except ImportError:
    gzip = None  # python can be built without zlib/gzip support


def make_transport(url):
    url_parts = urlparse(url)

    transport = ProxiedTransport()
    transport.set_proxy(url_parts.hostname, port=url_parts.port)

    return transport


class ProxiedTransport(xmlrpclib.Transport):
    def set_proxy(self, host, port=None, headers=None):
        self.proxy = (host, port)
        self.proxy_headers = headers

    def make_connection(self, host):
        if self._connection and host == self._connection[0]:
            return self._connection[1]

        connection = httplib.HTTPSConnection(*self.proxy)
        connection.set_tunnel(host, headers=self.proxy_headers)

        self._connection = (host, connection)
        return connection

    # workaround python httplib bug (#7776)
    if sys.version_info < (3, 0):
        def send_request(self, connection, handler, request_body):
            if (self.accept_gzip_encoding and gzip):
                connection.putrequest("POST", handler, skip_host=True, skip_accept_encoding=True)
                connection.putheader("Accept-Encoding", "gzip")
            else:
                connection.putrequest("POST", handler, skip_host=True)

        def send_host(self, connection, host):
            xmlrpclib.Transport.send_host(self, connection, host)

            if connection._tunnel_host:
                host = connection._tunnel_host
                port = connection._tunnel_port
            else:
                host = connection.host
                port = connection.port

            try:
                host_enc = host.encode("ascii")
            except UnicodeEncodeError:
                host_enc = host.encode("idna")
            # Wrap the IPv6 Host Header with [] (RFC 2732)
            if host_enc.find(':') >= 0:
                host_enc = "[" + host_enc + "]"
            if port == connection.default_port:
                connection.putheader('Host', host_enc)
            else:
                connection.putheader('Host', "%s:%s" % (host_enc, port))
