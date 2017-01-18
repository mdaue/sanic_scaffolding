"""
Initialize the Root

Recursively imports all directories' via their init functions.
Each __init__ module should define the following:
blueprints = [Blueprint1, Blueprint2...]

This init function will then dynamically import all the blueprint
environments with a cascading effect

Ignore non-blueprint directories using the IGNORE_NON_BLUEPRINTS
configuration item. Add essential APP_ARGS in the APP_ARGS variable

If the USE_SSL environmental variable is set, or the USE_SSL variable
is set to True, this will setup an SSL context and wrapper around
the socket.
"""

import asyncio
import glob
import importlib
import os
import ssl
import sys
import uvloop
from sanic import Sanic
from sanic.response import json

# CONFIG FILE SECTION:
IGNORE_NON_BLUEPRINTS = ["__", "templates", "ssl", ".", ".."]
APP_ARGS = {
    "host": "0.0.0.0",
    "port": 8443,
    "debug": True,
    "workers": 1,
    "loop": asyncio.get_event_loop()
}

SSL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ssl'))
SSL_CERT = os.path.join(SSL_PATH, 'server.crt')
SSL_KEY = os.path.join(SSL_PATH, 'server.key')
CIPHERS = 'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!MD5:!DSS'
USE_SSL = False

def create_ssl_context():
    """Creates an SSL context (TCP)

    :returns: SSLContext
    """
    # SSL:
    # - Create regular sockets with purpose=Purpose.CLIENT_AUTH
    # - Create server sockets with mandatory client verification, use the default
    #   of Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)  # Set CA certs here
    try:
        # Pass Certificate, Key and Password
        context.load_cert_chain(SSL_CERT, keyfile=SSL_KEY)  # password=None
        context.set_ciphers(CIPHERS)
    except ssl.SSLError as exc:
        print("Error importing cert chain {}/{}; exc={}".format(SSL_CERT, SSL_KEY, exc))
        return None

    return context  # ssl.SSLContext

# Enable SSL, either by setting the USE_SSL env var, or setting the USE_SSL var to True
if os.environ.get('USE_SSL') or USE_SSL is True:
    ssl_context = create_ssl_context()
    APP_ARGS['ssl'] = ssl_context

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic(__name__)

# Recursively import all directories
for root, dirs, files in os.walk(os.path.basename(os.path.dirname(__file__))):
    for dir_ in dirs:
        if True not in [True for x in IGNORE_NON_BLUEPRINTS if dir_.startswith(x)]:
            # Look for an __init__ file in the folder
            if not os.path.exists(os.path.join(root, dir_, '__init__.py')):
                continue
            abs_name = ".".join(root.split('/')) + '.' + dir_
            blueprint = importlib.import_module(abs_name)
            # Register blueprint
            if not getattr(blueprint, 'blueprints'):
                continue
            for bp in blueprint.blueprints:
                print("Registering blueprint: {}".format(bp.name))
                app.register_blueprint(bp)

app.run(**APP_ARGS)
