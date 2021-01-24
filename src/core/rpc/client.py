import json
import requests


class RPCDownException(Exception):
    pass


class RPCErrorResponseException(Exception):
    pass


def call(url, body):
    try:
        response = requests.post(url, body)
    except requests.ConnectionError:
        raise RPCDownException()

    if response.status_code == 200:
        return json.loads(response.content)
    else:
        raise RPCErrorResponseException(response.content.decode())


def call_with_progress(url, body, callback=None):
    try:
        with requests.post(url, body, stream=True) as response_stream:
            if response_stream.status_code != 200:
                raise RPCErrorResponseException()
            status = 'progress'
            body = ''

            for line in response_stream.iter_lines():
                line = line.decode()

                if line in ['done', 'failed']:
                    status = line
                    continue

                if status == 'progress' and callback is not None:
                    try:
                        data = float(line)
                    except Exception as e:
                        Exception("Unexpected RPC response")
                    callback(data)
                else:
                    body += line

            if status == 'done':
                return json.loads(body)
            elif status == 'failed':
                raise RPCErrorResponseException(body)

    except requests.ConnectionError:
        raise RPCDownException()
