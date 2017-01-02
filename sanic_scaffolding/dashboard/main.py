import asyncio
from sanic import Sanic, Blueprint
from sanic.response import json

dashboard_main = Blueprint('Main Dashboard', url_prefix='/main')

@dashboard_main.route('/')
async def main(request):
    return json({"main": 1})
