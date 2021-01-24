import bootstrap as bs
import logging
import aiohttp_cors
from aiohttp import web
from src.app.server.handlers import RPCExample, RPCProgressExample


# CONFIGURE APPLICATION
# init app and middlewares
app = web.Application()

# access log
# access_log = logging.getLogger('aiohttp.access')
# access_log.setLevel(logging.DEBUG)
# access_log.handlers = [logging.FileHandler(bs.path('var/access_log.txt'))]

# application log
application_log = logging.getLogger('application')
application_log.setLevel(logging.DEBUG)
application_log.handlers = [logging.StreamHandler()]


# endpoints go here
app.add_routes([
    web.get('/health-check', lambda r: web.Response(body='ok')),
    web.post('/examples-rpc', RPCExample().handle),
    web.post('/examples-rpc-progress', RPCProgressExample().handle),
])

# static
app.add_routes([
    web.static('/', bs.path('static'))
])

# configure CORS
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods="*"
    )
})

for resource in app.router.resources():
    cors.add(resource)

# start web server
async def on_startup(loop):
    pass


app.on_startup.append(on_startup)
web.run_app(app, port=bs.SERVER_PORT)
