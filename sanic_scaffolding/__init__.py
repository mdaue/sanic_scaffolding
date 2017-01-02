"""
Initialize the Root

Recursively imports all directories' via their init functions.
Each __init__ module should define the following:
blueprints = [Blueprint1, Blueprint2...]

This init function will then dynamically import all the blueprint
environments with a cascading effect

Ignore non-blueprint directories using the IGNORE_NON_BLUEPRINTS
configuration item. Add essential APP_ARGS in the APP_ARGS variable
"""

import asyncio
import glob
import importlib
import os
import uvloop
from sanic import Sanic
from sanic.response import json

# CONFIG FILE SECTION:
IGNORE_NON_BLUEPRINTS = ["__", "templates", ".", ".."]
APP_ARGS = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": True,
    "workers": 3,
    "loop": asyncio.get_event_loop()
}

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic(__name__)

# Recursively import all directories
for root, dirs, files in os.walk(os.path.basename(os.path.dirname(__file__))):
    for dir_ in dirs:
        if True not in [True for x in IGNORE_NON_BLUEPRINTS if dir_.startswith(x)]:
            abs_name = ".".join(root.split('/')) + '.' + dir_
            blueprint = importlib.import_module(abs_name)
            # Register blueprint
            for bp in blueprint.blueprints:
                print("Registering blueprint: {}".format(bp.name))
                app.register_blueprint(bp)

app.run(**APP_ARGS)
