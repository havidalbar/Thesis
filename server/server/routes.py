import aiohttp_cors
import os
from .controller import index, search
from aiohttp import web


def inject_routes(app: web.Application):
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/search', search)

    if int(os.getenv('IS_DEV', 1)) != 0:
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions()
        })

        for route in app.router.routes():
            cors.add(route)
