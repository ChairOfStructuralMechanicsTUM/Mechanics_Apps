# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
This example demonstrates how to run a reverse proxy.

Run this example with:
    $ python reverse-proxy.py

Then visit http://localhost:8080/ in your web browser.
"""

from twisted.internet import reactor
from twisted.web import proxy, server
from twisted.web.static import File

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input-port', required=True, help='port that is open to the web')
parser.add_argument('--bokeh-port', required=True, help='port where the bokeh server is running')
parser.add_argument('--global-ip', required=True, help='global ip of this machine')
args = parser.parse_args()

inputPort = int(args.input_port)
bokehPort = int(args.bokeh_port)
globalIP = args.global_ip

resource = File('./server_data/www/')
resource.putChild('apps',proxy.ReverseProxyResource(globalIP, bokehPort, ''))
resource.putChild('images',File('./server_data/images'))
resource.putChild('Diffraktion',File('./server_data/Diffraktion'))
resource.putChild('Diffraktion/images',File('./server_data/Diffraktion/images'))
resource.putChild('Diffraktion/static/images',File('./server_data/Diffraktion/static/images'))
site = server.Site(resource)
reactor.listenTCP(inputPort, site)
reactor.run()
