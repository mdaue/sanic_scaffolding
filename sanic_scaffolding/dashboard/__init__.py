import asyncio
from sanic import Sanic, Blueprint
from sanic.response import json
from .main import dashboard_main

blueprints = list()
dashboard_bp = Blueprint('Dashboard')  # no url prefix
# blueprint = Blueprint('Dashboard', url_prefix='/dashboard')

# All routes are setup here:
@dashboard_bp.route('/')
async def landing_point(request):
    return json({'landing': 1})

blueprints.append(dashboard_bp)

# Or imported:
blueprints.append(dashboard_main)
