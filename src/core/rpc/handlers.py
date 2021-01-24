import logging
import traceback
import sys
import json
from aiohttp import web
from src.core.rpc.parsers import JsonParser

logger = logging.getLogger('application')


class RPCHandler():
    name = 'Missed name'
    data_parser = JsonParser()

    def create_progress_cb(self, data, response):
        async def wrapper(progress):
            logger.info("%s: %s progress: %i" % (self.name, await self.data_parser.describe(data), progress * 100))
            await response.write(("%f\n" % progress).encode())

        return wrapper

    async def handle(self, request):
        data = await self.data_parser.parse(request)
        logger.info("%s %s started" % (self.name, await self.data_parser.describe(data)))

        response = web.StreamResponse(
            status=200,
            reason='OK',
            headers={'Content-Type': 'text/plain'},
        )
        await response.prepare(request)

        try:
            result = await self.create_coroutine(data, self.create_progress_cb(data, response))
        except Exception as e:
            traceback.print_exception(*(sys.exc_info()))
            await response.write('failed\n'.encode())
            await response.write(('Task "%s" failed.\n %s' % (self.name, e)).encode())
            await response.write_eof()
            return response
        logger.info("%s %s finished" % (self.name, await self.data_parser.describe(data)))

        await response.write('done\n'.encode())
        await response.write(json.dumps(result).encode())
        await response.write_eof()

        return response

    def create_coroutine(self, data, on_progress):
        raise NotImplemented()