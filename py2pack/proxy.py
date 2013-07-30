# -*- coding: utf-8 -*-
#
# Copyright (c) 2013, Sascha Peilicke <saschpe@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (see the file COPYING); if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

try:
    import http.client as httplib
except:
    import httplib
try:
    import xmlrpc.client as xmlrpclib
except:
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
