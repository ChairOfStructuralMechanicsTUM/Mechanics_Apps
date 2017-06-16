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
import os

parser = argparse.ArgumentParser()
parser.add_argument('--input-port', required=True, help='port that is open to the web')
parser.add_argument('--bokeh-port', required=True, help='port where the bokeh server is running')
parser.add_argument('--bokeh-port-testing', required=True, help='port where the bokeh server is running')
parser.add_argument('--global-ip', required=True, help='global ip of this machine')
args = parser.parse_args()

inputPort = int(args.input_port)
bokehPort = int(args.bokeh_port)
bokehPortTesting = int(args.bokeh_port_testing)
globalIP = args.global_ip

resource = File(os.path.dirname(__file__)+'/www/')
resource.putChild('apps',proxy.ReverseProxyResource(globalIP, bokehPort, ''))
resource.putChild('apps-testing',proxy.ReverseProxyResource(globalIP, bokehPortTesting, ''))
resource.putChild('images',File(os.path.dirname(__file__)+'/images'))
resource.putChild('Diffraktion',File(os.path.dirname(__file__)+'/Diffraktion'))
resource.putChild('Diffraktion/images',File(os.path.dirname(__file__)+'/Diffraktion/images'))
resource.putChild('Diffraktion/static/images',File(os.path.dirname(__file__)+'/Diffraktion/static/images'))
site = server.Site(resource)
reactor.listenTCP(inputPort, site)
reactor.run()
