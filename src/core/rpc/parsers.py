from src.core.utils.data import img_from_bytes


class DataParser:
    async def parse(self, request):
        raise NotImplemented()

    async def describe(self, data):
        raise NotImplemented()


class TextParser():
    async def parse(self, request):
        return await request.text()

    async def describe(self, data):
        return data


class JsonParser(DataParser):
    def __init__(self, key_describers={}, expose_data=True):
        self.key_describers = key_describers
        self.expose_data = expose_data

    async def parse(self, request):
        data = await request.json()

        return data

    async def describe(self, data):
        if not self.expose_data:
            return '[json]'

        pairs = []
        for key in data:
            value = data[key]
            if key in self.key_describers:
                value = self.key_describers[key](value)

            pairs.append(': '.join([key, str(value)]))

        return ' '.join(pairs)


class ImgParser(DataParser):
    async def parse(self, request):
        return img_from_bytes(await request.read())

    async def describe(self, data):
        return "img %ix%i" % (data.shape[1], data.shape[0])